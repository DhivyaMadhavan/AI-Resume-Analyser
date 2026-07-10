import DashboardCard from "./DashboardCard";

const WeaknessesCard = ({ analysis }) => {
  const weaknesses = analysis?.improvements || [];

  return (
    <DashboardCard title="Areas for Improvement">
      {weaknesses.length > 0 ? (
        <ul className="space-y-2">
          {weaknesses.map((item, index) => (
            <li key={index} className="flex items-start gap-2">
              <span className="text-red-500 font-bold">•</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-400 italic">
          No improvement suggestions available.
        </p>
      )}
    </DashboardCard>
  );
};

export default WeaknessesCard;