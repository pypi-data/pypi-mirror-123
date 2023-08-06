Object.defineProperty(exports, "__esModule", { value: true });
exports.loadFixtures = void 0;
const tslib_1 = require("tslib");
/* global __dirname */
/* eslint import/no-nodejs-modules:0 */
const fs_1 = (0, tslib_1.__importDefault)(require("fs"));
const path_1 = (0, tslib_1.__importDefault)(require("path"));
const FIXTURES_ROOT = path_1.default.join(__dirname, '../../fixtures');
/**
 * Loads a directory of fixtures. Supports js and json fixtures.
 */
function loadFixtures(dir, opts = {}) {
    const from = path_1.default.join(FIXTURES_ROOT, dir);
    const files = fs_1.default.readdirSync(from);
    const fixturesPairs = files.map(file => {
        const filePath = path_1.default.join(from, file);
        if (/[jt]sx?$/.test(file)) {
            const module = require(filePath);
            if (Object.keys(module).includes('default')) {
                throw new Error('Javascript fixtures cannot use default export');
            }
            return [file, module];
        }
        if (/json$/.test(file)) {
            return [file, JSON.parse(fs_1.default.readFileSync(filePath).toString())];
        }
        throw new Error(`Invalid fixture type found: ${file}`);
    });
    const fixtures = Object.fromEntries(fixturesPairs);
    if (opts.flatten) {
        return Object.values(fixtures).reduce((acc, val) => (Object.assign(Object.assign({}, acc), val)), {});
    }
    return fixtures;
}
exports.loadFixtures = loadFixtures;
//# sourceMappingURL=loadFixtures.js.map