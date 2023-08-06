Object.defineProperty(exports, "__esModule", { value: true });
function findBestThread(threads) {
    // search the entire threads list for a crashed thread with stack trace
    return (threads.find(thread => thread.crashed) ||
        threads.find(thread => thread.stacktrace) ||
        threads[0]);
}
exports.default = findBestThread;
//# sourceMappingURL=findBestThread.jsx.map