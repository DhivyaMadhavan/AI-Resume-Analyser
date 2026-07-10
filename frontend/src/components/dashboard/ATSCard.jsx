import DashboardCard from "./DashboardCard";

const ATSCard = ({ analysis }) => {
  const ats = analysis?.ats;

  if (!ats) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6 min-h-52">
        ATS data unavailable
      </div>
    );
  }

  const score = ats.overall_score;
  const maxScore = ats.max_score;

  const scoreColor =
    score >= 80
      ? "text-green-600"
      : score >= 60
      ? "text-yellow-500"
      : "text-red-600";

  const scoreLabel =
    score >= 80
      ? "Excellent Resume"
      : score >= 60
      ? "Good Resume"
      : score >= 40
      ? "Needs Improvement"
      : "Poor ATS Score";

   return (

    <DashboardCard title="ATS Score">

      <div className={`text-5xl font-bold ${scoreColor}`}>
        {score}
      </div>

      <p className="text-gray-500">
        out of {maxScore}
      </p>

      <div className="w-full bg-gray-200 rounded-full h-3 mt-6">
        <div
          className="bg-blue-600 h-3 rounded-full transition-all duration-500"
          style={{ width: `${score}%` }}
        />
      </div>

      <p className="mt-4 font-medium">
        {scoreLabel}
      </p>

    </DashboardCard>

  );
};

export default ATSCard;