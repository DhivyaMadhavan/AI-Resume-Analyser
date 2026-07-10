import DashboardCard from "./DashboardCard";

const RecommendationCard = ({ analysis }) => {
  const recommendations = analysis?.ats?.recommendations || [];

  return (
    <DashboardCard title="Recommendations">
      {recommendations.length > 0 ? (
        <ul className="space-y-2">
          {recommendations.map((item, index) => (
            <li key={index} className="flex items-start gap-2">
              <span className="text-blue-600">💡</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-400 italic">
          No recommendations available.
        </p>
      )}
    </DashboardCard>
  );
};

export default RecommendationCard;