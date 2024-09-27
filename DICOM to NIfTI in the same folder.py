#How to convert DICOM file into NIfTI and save the converted files in a the same directory
import os      # import os to walk through directories and files
import subprocess # import subprocess to run command line
import dcm2niix   # import dcm2niix to convert DICOM to NIfTI
import pydicom    # import pydicom to read DICOM files

print('Loop over dirs and files:')

source_path = r"\\?\R:\Projects\ai-amicus-brain-metastasis\DICOM\Task 10"


# How to define the function for conversion
def convert_dicom_to_nifti(nifti_output_directory, dicom_file_path):
    dicom_directory = os.path.dirname(dicom_file_path)
    file_name_format = f"{patient_id}_{sop_instance_uid}_{sequence_name}_{study_date}_{study_time}" # Define the file name format for the converted files
    command = f"dcm2niix -o \"{dicom_directory}\" -f {file_name_format} -z y \"{dicom_file_path}\"" # Define the command to convert the DICOM file to NIfTI
    subprocess.run(command, check=True, shell=True)


x = []  # To create an empty list


subdirs = [x[0] for x in os.walk(source_path)] # Get the list of subdirectories

# Loop over the subdirectories and files, and convert the DICOM files (with T1W sequence) to NIfTI
for subdir, dirs, files in os.walk(source_path):
    for subdir in subdirs:
        files = os.walk(subdir).__next__()[2]
        if (len(files) > 0):
            for file in files:
                file_path = os.path.join(subdir, file)
                try:
                    dataset = pydicom.dcmread(file_path)
                    patient_id = dataset.get('PatientID', None)
                    sop_instance_uid = dataset.get('SOPInstanceUID', None)
                    sequence_name = dataset.get('ScanningSequence', None)
                    study_date = dataset.get('StudyDate', None)
                    study_time = dataset.get('StudyTime', None)
                    if sequence_name == 'IR':  # represent T1W sequence
                        dicom_file_path = file_path # Define the address of the DICOM file to be converted
                        nifti_output_directory = subdir  # Define the output directory for the converted files
                        os.makedirs(nifti_output_directory, exist_ok=True) # Create the output directory if it does not exist
                        convert_dicom_to_nifti(nifti_output_directory, dicom_file_path)
                except Exception as e:
                    print(f"Error reading DICOM file {file_path}: {e}")


print("Conversion and decompression completed successfully.")
