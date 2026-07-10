function Navbar() {
  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-6xl mx-auto px-8 py-4 flex justify-between">

        <h1 className="text-2xl font-bold text-blue-700">
          AI Resume Analyzer
        </h1>

        <div className="space-x-6">
          <button className="text-gray-700 hover:text-blue-700">
            Home
          </button>

          <button className="text-gray-700 hover:text-blue-700">
            Dashboard
          </button>
        </div>

      </div>
    </nav>
  );
}

export default Navbar;