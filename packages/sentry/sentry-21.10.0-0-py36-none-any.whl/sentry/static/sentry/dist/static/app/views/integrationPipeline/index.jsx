function integrationPipeline() {
    return __awaiter(this, void 0, void 0, function* () {
        const { init } = yield Promise.resolve().then(() => __importStar(require('./init')));
        init();
    });
}
integrationPipeline();
//# sourceMappingURL=index.jsx.map