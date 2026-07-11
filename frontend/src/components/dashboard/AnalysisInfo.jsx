const AnalysisInfo = ({ resumeData }) => {
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
    <div className="bg-white rounded-xl shadow-md p-6 mb-6">

      <h2 className="text-xl font-semibold mb-5">
        Processing Information
      </h2>

      <div className="space-y-5">

        {/* Resume Analysis */}

        <div>

          <p className="font-semibold text-gray-800">
            📄 Resume Analysis
          </p>

          <p className="text-gray-600 ml-5 mt-1">
            {resumeInfo.icon} {resumeInfo.text}
          </p>

        </div>

        {/* JD / Role Matching */}

        {matchingSource && (

          <div>

            <p className="font-semibold text-gray-800">

              {resumeData.matching.mode === "jd"
                ? "🎯 JD Matching"
                : "🎯 Role Matching"}

            </p>

            <p className="text-gray-600 ml-5 mt-1">
              {matchingInfo.icon} {matchingInfo.text}
            </p>

          </div>

        )}

        {/* Resume Hash */}

        <div className="border-t pt-4">

          <p className="font-semibold text-gray-800">
            Resume Hash
          </p>

          <p className="text-sm text-gray-500 break-all mt-1">
            {resumeHash}
          </p>

        </div>

      </div>

    </div>
  );
};

export default AnalysisInfo;