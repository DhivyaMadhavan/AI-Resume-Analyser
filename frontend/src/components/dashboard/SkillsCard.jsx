import DashboardCard from "./DashboardCard";

const SkillsCard = ({ analysis }) => {
  const skills = analysis?.skills || [];

  return (
    <DashboardCard title="Skills">
      {skills.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {skills.map((skill, index) => (
            <span
              key={index}
              className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm"
            >
              {skill}
            </span>
          ))}
        </div>
      ) : (
        <p className="text-gray-400 italic">
          No skills detected.
        </p>
      )}
    </DashboardCard>
  );
};

export default SkillsCard;