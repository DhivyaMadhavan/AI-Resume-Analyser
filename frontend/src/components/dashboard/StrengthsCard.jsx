import DashboardCard from "./DashboardCard";

const StrengthsCard = ({ analysis }) => {
  const strengths = analysis?.strengths || [];

  return (
    <DashboardCard title="Strengths">
      {strengths.length > 0 ? (
        <ul className="space-y-2">
          {strengths.map((strength, index) => (
            <li key={index} className="flex items-start gap-2">
              <span className="text-green-600 font-bold">✓</span>
              <span>{strength}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-400 italic">
          No strengths identified.
        </p>
      )}
    </DashboardCard>
  );
};

export default StrengthsCard;