# Material ZERO 
### 3D printer software for hands free and convenient printing (V1.0.0)

This gives a web interface for uploading files and remotely monitoring prints.

Files are uploaded to a raspberry Pi via a flask app. Uploaded files are automatically sliced (with support structures if applicable and automatic infills)

On the user side:
- Files are to be uploaded (.stl files), already repaired
- One of 3 presets are to be selected (Fast printing with low resolution, Balanced, or High res with slow printing)
- That's it! Ongoing prints can be monitored remotely from anywhere.