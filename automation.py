import os
import subprocess

# Paths
faces_dir = '/Users/Tom/LivePortrait/faces'
pkl_dir = '/Users/Tom/LivePortrait/videos'
output_base_dir = '/Users/Tom/LivePortrait/foutputs'

# List of -d files you specified
d_files = ['F01.pkl', 'F02.pkl', 'F03.pkl', 'F04.pkl', 'F05.pkl',
           'M02.pkl', 'M03.pkl', 'M04.pkl', 'M06.pkl', 'M08.pkl', 'M11.pkl', 'M12.pkl']

# Get all .jpeg files from faces directory
s_files = [f for f in os.listdir(faces_dir) if f.lower().endswith('.jpeg')]

# Loop through all combinations
for s_file in s_files:
    s_path = os.path.join(faces_dir, s_file)
    s_name = os.path.splitext(s_file)[0]

    output_dir = os.path.join(output_base_dir, f'foutputs_{s_name}')
    os.makedirs(output_dir, exist_ok=True)

    for d_file in d_files:
        d_path = os.path.join(pkl_dir, d_file)
        d_name = os.path.splitext(d_file)[0]

        # Run the inference.py script
        cmd = [
            'PYTORCH_ENABLE_MPS_FALLBACK=1', 'python', 'inference.py',
            '-s', s_path,
            '-d', d_path
        ]
        print(f'Running: {" ".join(cmd)}')
        subprocess.run(' '.join(cmd), shell=True, check=True)

        # Move the resulting mp4 to the correct output dir
        output_mp4_name = f'{s_name}--{d_name}.mp4'
        generated_mp4_path = f'/Users/Tom/LivePortrait/animations/{output_mp4_name}'

        if os.path.exists(generated_mp4_path):
            final_output_path = os.path.join(output_dir, output_mp4_name)
            os.rename(generated_mp4_path, final_output_path)
            print(f'Moved {generated_mp4_path} to {final_output_path}')
        else:
            print(f'Warning: {generated_mp4_path} not found.')

print("All processing complete.")
