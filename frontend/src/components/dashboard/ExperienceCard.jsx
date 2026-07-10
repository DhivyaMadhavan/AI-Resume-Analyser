import DashboardCard from "./DashboardCard";

const ExperienceCard = ({ analysis }) => {
  const exp = analysis?.experience_summary;

  if (!exp) {
    return (
      <DashboardCard title="Experience">
        <p className="text-gray-400 italic">
          Experience unavailable
        </p>
      </DashboardCard>
    );
  }

  return (
    <DashboardCard title="Experience">
      <div className="space-y-4">
        <div>
          <p className="text-sm text-gray-500">
            Total Experience
          </p>

          <p className="font-semibold text-lg">
            {exp.total_experience}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            IT Experience
          </p>

          <p className="font-medium">
            {exp.it_experience}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">
            Non-IT Experience
          </p>

          <p className="font-medium">
            {exp.non_it_experience}
          </p>
        </div>
      </div>
    </DashboardCard>
  );
};

export default ExperienceCard;