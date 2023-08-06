Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const modalManager_1 = (0, tslib_1.__importDefault)(require("./modalManager"));
const Add = (_a) => {
    var { savedRules } = _a, props = (0, tslib_1.__rest)(_a, ["savedRules"]);
    const handleGetNewRules = (values) => {
        return [...savedRules, Object.assign(Object.assign({}, values), { id: savedRules.length })];
    };
    return (<modalManager_1.default {...props} savedRules={savedRules} title={(0, locale_1.t)('Add an advanced data scrubbing rule')} onGetNewRules={handleGetNewRules}/>);
};
exports.default = Add;
//# sourceMappingURL=add.jsx.map