import { useState } from "react"

import axios from 'axios';

export function FileUpload() {
    const [selectedFile, setSelectedFile] = useState<File>();

    
    const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if(event.currentTarget.files) {
            setSelectedFile(event.currentTarget.files[0]);
        }
    }

    // On file upload (click the upload button)
    const onFileUpload = () => {
     
      // Create an object of formData
      const formData = new FormData();
     
      if(selectedFile) {
        // Update the formData object
        formData.append(
            "uploaded_file",
            selectedFile
        );
        
        const headers={'Content-Type':  selectedFile.type}
        const config= {
            headers: headers
        }

        console.log(formData)

        axios.post("http://127.0.0.1:8000/files", formData, config)

      }
    };

    return(
        <div>
            <form>
            <label className="block mb-2 text-sm font-medium text-gray-900 dark:text-white" htmlFor="file_input">Upload file</label>
            <input 
                className="
                    block w-full 
                    file:text-sm 
                    file:text-gray-900 border 
                    file:border-gray-300 
                    rounded-lg 
                    file:cursor-pointer 
                    bg-gray-50 
                    dark:text-gray-400 
                    focus:outline-none 
                    file:dark:bg-gray-700 
                    file:dark:border-gray-600 
                    file:dark:placeholder-gray-400"
                id="file_input" 
                type="file"
                onChange={onFileChange}
            />
            <button 
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
                onClick={onFileUpload}
            >
                Upload
            </button>
            </form>
        </div>
    )
}