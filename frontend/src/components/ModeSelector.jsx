function ModeSelector({ mode, setMode }) {
  return (
    <div className="grid md:grid-cols-3 gap-5">

      <div
        onClick={() => setMode("resume")}
        className={`cursor-pointer rounded-xl p-6 border-2 ${
          mode === "resume"
            ? "border-blue-600 bg-blue-50"
            : "border-gray-300 bg-white"
        }`}
      >
        <h2 className="text-xl font-bold">
          Resume Analysis
        </h2>

        <p className="text-gray-600 mt-2">
          ATS Score and Resume Review
        </p>
      </div>

      <div
        onClick={() => setMode("jd")}
        className={`cursor-pointer rounded-xl p-6 border-2 ${
          mode === "jd"
            ? "border-blue-600 bg-blue-50"
            : "border-gray-300 bg-white"
        }`}
      >
        <h2 className="text-xl font-bold">
          JD Matching
        </h2>

        <p className="text-gray-600 mt-2">
          Compare Resume with Job Description
        </p>
      </div>

      <div
        onClick={() => setMode("role")}
        className={`cursor-pointer rounded-xl p-6 border-2 ${
          mode === "role"
            ? "border-blue-600 bg-blue-50"
            : "border-gray-300 bg-white"
        }`}
      >
        <h2 className="text-xl font-bold">
          Role Matching
        </h2>

        <p className="text-gray-600 mt-2">
          Compare Resume with Job Role
        </p>
      </div>

    </div>
  );
}

export default ModeSelector;