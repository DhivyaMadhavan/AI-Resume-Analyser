import { useState } from "react";

const AnalysisInfo = ({ resumeData }) => {

  const [showInfo, setShowInfo] = useState(false);  
  if (!resumeData) return null;

  // Resume analysis source (top-level)
  const resumeSource = resumeData?.source;

  // JD / Role matching source
  const matchingSource = resumeData?.matching?.metadata?.source;

  const resumeHash = resumeData?.resume_hash;

  const getSourceInfo = (source) => {
    switch (source) {
      case "fresh_analysis":
        return {
          icon: "🤖",
          text: "Fresh AI Analysis",
        };

      case "redis":
        return {
          icon: "⚡",
          text: "Redis Cache",
        };

      case "mongodb":
        return {
          icon: "💾",
          text: "MongoDB",
        };

      default:
        return {
          icon: "❓",
          text: "Unknown",
        };
    }
  };

  const resumeInfo = getSourceInfo(resumeSource);
  const matchingInfo = getSourceInfo(matchingSource);

  return (
  <div className="mb-4">
    {/* Toggle Button */}
    <button
      onClick={() => setShowInfo(!showInfo)}
      className="flex items-center gap-2 rounded-md border border-gray-300 bg-gray-50 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-100 transition"
    >
      ⚙️ Processing Info
      <span>{showInfo ? "▲" : "▼"}</span>
    </button>

    {/* Expandable Card */}
    {showInfo && (
      <div className="mt-2 w-fit max-w-sm rounded-lg border border-gray-200 bg-white p-3 shadow-sm text-[11px]">

        <div className="space-y-3">

          {/* Resume */}
          <div>
            <p className="font-semibold text-gray-800">
              📄 Resume Analysis
            </p>

            <p className="ml-5 text-gray-600">
              {resumeInfo.icon} {resumeInfo.text}
            </p>
          </div>

          {/* JD / Role */}
          {matchingSource && (
            <div>
              <p className="font-semibold text-gray-800">
                {resumeData.matching.mode === "jd"
                  ? "🎯 JD Matching"
                  : "🎯 Role Matching"}
              </p>

              <p className="ml-5 text-gray-600">
                {matchingInfo.icon} {matchingInfo.text}
              </p>
            </div>
          )}         

        </div>
      </div>
    )}
  </div>
);
};

export default AnalysisInfo;