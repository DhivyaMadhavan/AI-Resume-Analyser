const Loader = () => {
  return (
    <div className="fixed inset-0 z-50 bg-white flex flex-col items-center justify-center">

      <div className="h-16 w-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>

      <h2 className="mt-6 text-2xl font-semibold">
        Analyzing Resume
      </h2>

      <p className="mt-2 text-gray-600">
        Please wait while AI processes your resume...
      </p>

    </div>
  );
};

export default Loader;