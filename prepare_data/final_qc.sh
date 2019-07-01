#!/bin/bash
#
# Delete temporary files. Run this script once all files have been verified.
# Usage:
#   ./delete_temp_files.sh <SUBJECT> <PATH_OUTPUT> <PATH_QC> <PATH_LOG> <TO_EXCLUDE>
#
# -x: Full verbose, -e: Exit if error
# set -x


# PARAMETERS & VARIABLES
# ==============================================================================

# Retrieve input params
SUBJECT=$1
PATH_OUTPUT=$2
PATH_QC=$3
PATH_LOG=$4
TO_EXCLUDE=$5

# Create BIDS architecture
PATH_IN="`pwd`/${SUBJECT}/anat"
ofolder_seg="${PATH_OUTPUT}/derivatives/labels/${SUBJECT}/anat"
ofolder_reg="${PATH_OUTPUT}/${SUBJECT}/anat"

# Set filenames
file_t1w_mts="${SUBJECT}_acq-T1w_MTS"
file_mton="${SUBJECT}_acq-MTon_MTS"
file_mtoff="${SUBJECT}_acq-MToff_MTS"
file_t2w="${SUBJECT}_T2w"
file_t2s="${SUBJECT}_T2star"
file_t1w="${SUBJECT}_T1w"

FILES_SRC=(
  "${file_t1w_mts}_crop_r"
  "${file_mton}_reg"
  "${file_mtoff}_reg"
  "${file_t2w}_reg2"
  "${file_t2s}_reg2"
  "${file_t1w}_reg2"
)

FILES_DEST=(
  "${file_t1w_mts}"
  "${file_mton}"
  "${file_mtoff}"
  "${file_t2w}"
  "${file_t2s}"
  "${file_t1w}"
)



# FUNCTIONS
# ==============================================================================

contains() {
  [[ $1 =~ (^|[[:space:]])$2($|[[:space:]]) ]] && echo 0 || echo 1
}



# SCRIPT STARTS HERE
# ==============================================================================

# echo $TO_EXCLUDE
# echo "TESTING $file_mtoff:"
# contains $TO_EXCLUDE $file_mtoff
# echo "RESULTS: $?"
# exit 0

# Go to output anat folder, where most of the outputs will be located
cd ${ofolder_reg}

# Copy files to appropriate locations
# cp tmp/${file_t1w_mts}_crop_r.nii.gz ${file_t1w_mts}.nii.gz
# cp tmp/${file_mton}_reg.nii.gz ${file_mton}.nii.gz
# cp tmp/${file_mtoff}_reg.nii.gz ${file_mtoff}.nii.gz

# Rename current files (remove "_reg")
# mv ${file_t1w}_reg.nii.gz ${file_t1w}.nii.gz
# mv ${file_t2w}_reg.nii.gz ${file_t2w}.nii.gz
# mv ${file_t2s}_reg.nii.gz ${file_t2s}.nii.gz

for i in ${!FILES_SRC[@]}; do
  # Copy and rename file
  cp tmp/${FILES_SRC[$i]}.nii.gz ${FILES_DEST[$i]}.nii.gz
  # Duplicate segmentation to be used by other contrasts
  cp tmp/${file_t1w_mts}_crop_r_seg-manual.nii.gz ${ofolder_seg}/${FILES_DEST[$i]}_seg-manual.nii.gz
  # Remove empty slices at the edge
  prepdata -i ${FILES_DEST[$i]}.nii.gz -s ${ofolder_seg}/${FILES_DEST[$i]}_seg-manual.nii.gz remove-slice
  # Generate final QC
  sct_qc -i ${FILES_DEST[$i]}.nii.gz -s ${ofolder_seg}/${FILES_DEST[$i]}_seg-manual.nii.gz -p sct_deepseg_sc -qc ${PATH_QC}2 -qc-subject ${SUBJECT}
  # Copy json file and rename them
  cp ${PATH_IN}/${FILES_DEST[$i]}.json ${FILES_DEST[$i]}.json
done

# TODO: Copy the following json files:
# Copy json files and rename them
# cp ${PATH_IN}/../../dataset_description.json ../../
# cp ${PATH_IN}/../../participants.json ../../
# cp ${PATH_IN}/../../participants.tsv ../../
