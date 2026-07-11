import DashboardCard from "./DashboardCard";

const ATSCard = ({ analysis }) => {

  const ats = analysis?.ats;

  if (!ats) {
    return (
      <DashboardCard title="ATS Score">
        <p className="text-gray-500">
          ATS data unavailable
        </p>
      </DashboardCard>
    );
  }

  const score = ats.overall_score;

  const scoreColor =
    score >= 80
      ? "text-green-600 border-green-500"
      : score >= 60
      ? "text-yellow-500 border-yellow-500"
      : "text-red-600 border-red-500";

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

      <div className="flex flex-col items-center">

        {/* Circular Score */}
        <div
          className={`
            w-32 
            h-32 
            rounded-full 
            border-8 
            ${scoreColor}
            flex 
            flex-col 
            items-center 
            justify-center
          `}
        >
          <span className="text-4xl font-bold">
            {score}%
          </span>

          <span className="text-sm text-gray-500">
            ATS
          </span>

        </div>


        {/* Status */}
        <p className="mt-5 font-medium">
          {scoreLabel}
        </p>


        {/* Progress bar */}
        <div className="w-full bg-gray-200 rounded-full h-3 mt-5">

          <div
            className="bg-blue-600 h-3 rounded-full transition-all duration-500"
            style={{
              width: `${score}%`
            }}
          />

        </div>

      </div>

    </DashboardCard>

  );
};

export default ATSCard;