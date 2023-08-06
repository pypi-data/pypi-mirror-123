Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const locale_1 = require("app/locale");
const modalManager_1 = (0, tslib_1.__importDefault)(require("./modalManager"));
const Edit = (_a) => {
    var { savedRules, rule } = _a, props = (0, tslib_1.__rest)(_a, ["savedRules", "rule"]);
    const handleGetNewRules = (values) => {
        const updatedRule = Object.assign(Object.assign({}, values), { id: rule.id });
        const newRules = savedRules.map(savedRule => {
            if (savedRule.id === updatedRule.id) {
                return updatedRule;
            }
            return savedRule;
        });
        return newRules;
    };
    return (<modalManager_1.default {...props} savedRules={savedRules} title={(0, locale_1.t)('Edit an advanced data scrubbing rule')} initialState={rule} onGetNewRules={handleGetNewRules}/>);
};
exports.default = Edit;
//# sourceMappingURL=edit.jsx.map