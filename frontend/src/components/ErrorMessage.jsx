function ErrorMessage({ message }) {

    if (!message) return null;

    return (
        <div className="mt-6 p-4 rounded-xl bg-red-50 border border-red-200 text-red-700">

            <div className="font-semibold">
                ❌ Error
            </div>

            <p className="mt-1">
                {message}
            </p>

        </div>
    );
}

export default ErrorMessage;