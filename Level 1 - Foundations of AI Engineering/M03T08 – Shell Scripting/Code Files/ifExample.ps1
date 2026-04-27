if (Test-Path -Path "new_folder"){
    New-Item -ItemType Directory -Path "if_folder" 
}

if (Test-Path -Path "if_folder"){
    New-Item -ItemType Directory -Path "hyperionDev"
} else {
    New-Item -ItemType Directory -Path "new-projects"
}