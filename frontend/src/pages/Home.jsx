import { useState } from "react";

import Navbar from "../components/Navbar";
import ModeSelector from "../components/ModeSelector";
import UploadBox from "../components/UploadBox";

import useResumeAnalysis from "../hooks/useResumeAnalysis";
import Loader from "../components/Loader";
import ErrorMessage from "../components/ErrorMessage";

function Home() {
  const [mode, setMode] = useState("resume");
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [role, setRole] = useState("");

  const { analyze, loading, error } = useResumeAnalysis();

  // Show full-screen loader
  if (loading) {
    return <Loader />;
  }

  return (
    <>
      <Navbar />

      <div className="max-w-5xl mx-auto mt-10">
        <h1 className="text-5xl font-bold text-center">
          AI Resume Analyzer
        </h1>

        <p className="text-center mt-4 text-gray-600">
          Analyze • Match • Optimize your Resume
        </p>

        <div className="mt-12">
          <ModeSelector
            mode={mode}
            setMode={setMode}
          />
        </div>

        <div className="mt-10 bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold">
            Upload Resume
          </h2>

          <UploadBox
            file={file}
            setFile={setFile}
          />

          {mode === "jd" && (
            <div className="mt-8">
              <label className="font-semibold">
                Paste Job Description
              </label>

              <textarea
                rows={8}
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                className="w-full mt-3 border rounded-lg p-4"
              />
            </div>
          )}

          {mode === "role" && (
            <div className="mt-8">
              <label className="font-semibold">
                Select Role
              </label>

              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full mt-3 border rounded-lg p-3"
              >
                <option value="">Select Role</option>
                <option>Backend Developer</option>
                <option>Frontend Developer</option>
                <option>Full Stack Developer</option>
                <option>Python Developer</option>
                <option>Data Scientist</option>
                <option>AI Engineer</option>
                <option>Machine Learning Engineer</option>
                <option>DevOps Engineer</option>
              </select>
            </div>
          )}

          <ErrorMessage message={error} />

          <button
            onClick={() =>
              analyze({
                file,
                mode,
                jobDescription,
                role,
              })
            }
            disabled={loading}
            className={`mt-8 w-full text-white py-4 rounded-xl text-lg ${
              loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            Analyze Resume
          </button>
        </div>
      </div>
    </>
  );
}

export default Home;