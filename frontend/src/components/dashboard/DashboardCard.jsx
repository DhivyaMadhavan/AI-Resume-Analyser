const DashboardCard = ({ title, children, minHeight = "min-h-52" }) => {
  return (
    <div className={`bg-white rounded-xl shadow-md p-6 ${minHeight}`}>
      <h2 className="text-xl font-semibold mb-5">
        {title}
      </h2>

      {children}
    </div>
  );
};

export default DashboardCard;