Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const groupingComponent_1 = (0, tslib_1.__importDefault)(require("./groupingComponent"));
const groupingComponentFrames_1 = (0, tslib_1.__importDefault)(require("./groupingComponentFrames"));
const utils_1 = require("./utils");
const GroupingComponentStacktrace = ({ component, showNonContributing }) => {
    const getFrameGroups = () => {
        const frameGroups = [];
        component.values
            .filter(value => (0, utils_1.groupingComponentFilter)(value, showNonContributing))
            .forEach(value => {
            const key = value.values
                .filter(v => (0, utils_1.groupingComponentFilter)(v, showNonContributing))
                .map(v => v.id)
                .sort((a, b) => a.localeCompare(b))
                .join('');
            const lastGroup = frameGroups[frameGroups.length - 1];
            if ((lastGroup === null || lastGroup === void 0 ? void 0 : lastGroup.key) === key) {
                lastGroup.data.push(value);
            }
            else {
                frameGroups.push({ key, data: [value] });
            }
        });
        return frameGroups;
    };
    return (<react_1.Fragment>
      {getFrameGroups().map((group, index) => (<groupingComponentFrames_1.default key={index} items={group.data.map((v, idx) => (<groupingComponent_1.default key={idx} component={v} showNonContributing={showNonContributing}/>))}/>))}
    </react_1.Fragment>);
};
exports.default = GroupingComponentStacktrace;
//# sourceMappingURL=groupingComponentStacktrace.jsx.map