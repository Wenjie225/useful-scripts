#How to convert DICOM file into NIfTI and store the converted files in a new directory
import os      # import os to walk through directories and files
import subprocess # import subprocess to run command line
import dcm2niix   # import dcm2niix to convert DICOM to NIfTI
import pydicom    # import pydicom to read DICOM files

print('Loop over dirs and files:')

source_path = r"\\?\R:\Projects\ai-amicus-brain-metastasis\DICOM\Task 13"
target_path = r'R:\Projects\ai-amicus-brain-metastasis\Conversion Output'


# How to define the function for conversion
def convert_dicom_to_nifti(nifti_output_directory, dicom_file_path):
    file_name_format = f"{patient_id}_{sop_instance_uid}_{sequence_name}_{study_date}_{study_time}"
    command = f"dcm2niix -o \"{nifti_output_directory}\" -f {file_name_format} -z y \"{dicom_file_path}\""
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
                        relative_dir = os.path.relpath(subdir, source_path)  # Get the relative path of the current directory, but need to copy the directory path from patient ID to a specific MR study
                        nifti_output_directory = os.path.join(target_path, relative_dir)  # Define the output directory for the converted files
                        os.makedirs(nifti_output_directory, exist_ok=True) # Create the output directory if it does not exist
                        convert_dicom_to_nifti(nifti_output_directory, dicom_file_path)  # Convert the DICOM file to NIfTI
                except Exception as e:
                    print(f"Error reading DICOM file {file_path}: {e}")



print("Conversion completed successfully.")
