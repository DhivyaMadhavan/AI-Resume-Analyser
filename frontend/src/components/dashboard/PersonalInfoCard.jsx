import DashboardCard from "./DashboardCard";

const PersonalInfoCard = ({ analysis }) => {
  const details = analysis?.personal_details;
  const candidate = analysis?.candidate;

  if (!details) {
    return (
      <DashboardCard title="Personal Information">
        <p className="text-gray-400 italic">
          Personal information unavailable
        </p>
      </DashboardCard>
    );
  }

  return (
    <DashboardCard title="Personal Information">
      <div className="space-y-4">

        <div>
          <p className="text-sm text-gray-500">Name</p>
          <p className="font-medium">
            {candidate?.name || "Not Available"}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Email</p>
          <p className="font-medium">
            {details.email || "Not Available"}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Phone</p>
          <p className="font-medium">
            {details.phone || "Not Available"}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-500">LinkedIn</p>

          {details.linkedin ? (
            <p className="font-medium">{details.linkedin}</p>
          ) : (
            <p className="text-gray-400 italic">Not Available</p>
          )}
        </div>

        <div>
          <p className="text-sm text-gray-500">GitHub</p>

          {details.github ? (
            <p className="font-medium">{details.github}</p>
          ) : (
            <p className="text-gray-400 italic">Not Available</p>
          )}
        </div>

      </div>
    </DashboardCard>
  );
};

export default PersonalInfoCard;