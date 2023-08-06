Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const platforms_1 = (0, tslib_1.__importDefault)(require("app/data/platforms"));
function getPlatformName(platform) {
    const platformData = platforms_1.default.find(({ id }) => platform === id);
    return platformData ? platformData.name : null;
}
exports.default = getPlatformName;
//# sourceMappingURL=getPlatformName.jsx.map