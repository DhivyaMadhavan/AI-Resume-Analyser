import { useDropzone } from "react-dropzone";

function UploadBox({ file, setFile }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "application/pdf": [".pdf"],
    },

    multiple: false,

    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
      }
    },
  });

  return (
    <div
      {...getRootProps()}
      className={`mt-6 h-60 rounded-xl border-2 border-dashed flex flex-col items-center justify-center cursor-pointer transition

      ${
        isDragActive
          ? "border-blue-600 bg-blue-50"
          : "border-gray-400 bg-gray-50"
      }`}
    >
      <input {...getInputProps()} />

      {file ? (
        <div className="relative w-full h-full flex flex-col items-center justify-center">

            <button
            onClick={(e) => {
                e.stopPropagation();      // Prevent opening file picker
                setFile(null);
            }}
            className="absolute top-4 right-4 w-8 h-8 rounded-full bg-red-500 text-white hover:bg-red-600 transition"
            >
            ✕
            </button>

            <h3 className="text-xl font-semibold text-green-600">
            ✅ File Selected
            </h3>

            <p className="mt-3 font-medium">
            {file.name}
            </p>

            <p className="text-gray-500 mt-1">
            {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>

            <p className="mt-5 text-sm text-blue-600">
            Click ✕ to remove and upload another file
            </p>

        </div>
        ) : (
        <>
          <h3 className="text-xl font-semibold">
            Drag & Drop Resume Here
          </h3>

          <p className="mt-3 text-gray-500">
            or click to browse
          </p>

          <p className="mt-2 text-sm text-gray-400">
            PDF files only
          </p>
        </>
      )}
    </div>
  );
}

export default UploadBox;