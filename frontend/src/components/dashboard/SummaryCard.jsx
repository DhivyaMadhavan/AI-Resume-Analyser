import DashboardCard from "./DashboardCard";

const SummaryCard = ({ analysis }) => {
  const summary = analysis?.candidate?.summary;

  return (
    <DashboardCard title="Resume Summary">
      {summary ? (
        <p className="text-gray-700 leading-7">
          {summary}
        </p>
      ) : (
        <p className="text-gray-400 italic">
          Summary not available.
        </p>
      )}
    </DashboardCard>
  );
};

export default SummaryCard;