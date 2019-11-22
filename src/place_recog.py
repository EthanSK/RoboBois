#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import os
import copy

# Location signature class: stores a signature characterizing one location


class LocationSignature:
    def __init__(self, no_bins=360):
        self.sig = [0] * no_bins

    def print_signature(self):
        for i in range(len(self.sig)):
            print(self.sig[i])

# --------------------- File management class ---------------


class SignatureContainer():
    def __init__(self, size=5):
        self.size = size  # max number of signatures that can be stored
        self.filenames = []

        # Fills the filenames variable with names like loc_%%.dat
        # where %% are 2 digits (00, 01, 02...) indicating the location number.
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are
    # used, it returns -1
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1

        if (n >= self.size):
            return -1
        else:
            return n

    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print("STATUS:  All signature files removed.")
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])

    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)

        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close()

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = LocationSignature()
        filename = self.filenames[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline()
                if (s != ''):
                    ls.sig[i] = int(s)
            f.close()
        else:
            print("WARNING: Signature does not exist.")

        return ls


def characterize_location(robot):
    readings = robot.sensor_module.get_sonar_full_rotation()
    ls = LocationSignature(len(readings))
    for i in range(len(readings)):
        ls.sig[i] = readings[i][1]  # store distance for each rotation
    return ls


def convert_sig_to_rot_invariant(ls):
    new_ls = LocationSignature(256)
    for i in range(len(ls.sig)):
        new_ls.sig[ls.sig[i]] += 1  # count num occurences of distance
    return new_ls


# compare two signatures
def compare_signatures(ls1, ls2):
    dist = 0
    if len(ls1.sig) != len(ls2.sig):
        raise Exception(
            "The lengths of the two signatures being compared are different")
    for i in range(len(ls1.sig)):
        dist += (ls1.sig[i] - ls2.sig[i]) ** 2
    return dist

# calculate the shift in degrees between two signatures (histograms of distance against rotation)


def calc_sig_shift_degrees(ls1, ls2):
    min_dist = float('inf')
    shift_at_min_dist = 0
    sliding_ls = copy.copy(ls1)
    if len(ls1.sig) != len(ls2.sig):
        raise Exception(
            "The lengths of the two signatures being compared are different")
    # need to slide one signature over the other, and calculate the min dist at every slide delta
    # When sliding (ls1 over ls2), values over 360 should wrap around. should do the shift 360 times
    for shift in range(len(ls1.sig)):
        dist = compare_signatures(sliding_ls, ls2)
        if dist < min_dist:
            min_dist = dist
            shift_at_min_dist = shift
        # rotate
        sliding_ls.sig = ls1.sig[shift:] + ls1.sig[:shift]
    return shift_at_min_dist

# This function characterizes the current location, and stores the obtained
# signature into the next available file.


def learn_location(robot, signatures):
    ls = characterize_location(robot)

    idx = signatures.get_free_index()
    if (idx == -1):  # run out of signature files
        print("\nWARNING:")
        print("No signature file is available. NOTHING NEW will be learned and stored.")
        print("Please remove some loc_%%.dat files.\n")
        return

    signatures.save(ls, idx)
    print("STATUS:  Location " + str(idx) + " learned and saved.")


# This function tries to recognize the current location.
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen

def recognize_location(robot, signatures, is_rotation_invariant=True):
    ls_obs = characterize_location(robot)
    
    if is_rotation_invariant:
        ls_obs_invariant = convert_sig_to_rot_invariant(ls_obs)

    #  COMPARE ls_read with ls_obs and find the best match
    min_dist = float('inf')
    for idx in range(signatures.size):
        print("STATUS:  Comparing signature " +
              str(idx) + " with the observed signature.")
        ls_read = signatures.read(idx)

        if is_rotation_invariant:
            ls_read_invariant = convert_sig_to_rot_invariant(ls_read)
            dist = compare_signatures(ls_obs_invariant, ls_read_invariant)
        else:
            dist = compare_signatures(ls_obs, ls_read)

        if dist < min_dist:
            min_dist = dist
            min_index = idx
            min_ls_read = ls_read
    # print("ls obs:", len(ls_obs.sig), ls_obs.sig, "ls read: ", len(min_ls_read.sig), min_ls_read.sig)
    shift = calc_sig_shift_degrees(ls_obs, min_ls_read)
    print("Index of closest signature match: ", min_index, "shift: ", shift)
    return (min_index, shift)
# Prior to starting learning the locations, it should delete files from previous
# learning either manually or by calling signatures.delete_loc_files().
# Then, either learn a location, until all the locations are learned, or try to
# recognize one of them, if locations have already been learned.

# signatures = SignatureContainer(5)
# # signatures.delete_loc_files()

# learn_location()
# recognize_location()
