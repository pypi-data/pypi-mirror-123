Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const isObject_1 = (0, tslib_1.__importDefault)(require("lodash/isObject"));
const groupingComponent_1 = (0, tslib_1.__importStar)(require("./groupingComponent"));
const utils_1 = require("./utils");
const GroupingComponentChildren = ({ component, showNonContributing }) => {
    return (<react_1.Fragment>
      {component.values
            .filter(value => (0, utils_1.groupingComponentFilter)(value, showNonContributing))
            .map((value, idx) => (<groupingComponent_1.GroupingComponentListItem key={idx}>
            {(0, isObject_1.default)(value) ? (<groupingComponent_1.default component={value} showNonContributing={showNonContributing}/>) : (<groupingComponent_1.GroupingValue valueType={component.name || component.id}>
                {typeof value === 'string' || typeof value === 'number'
                    ? value
                    : JSON.stringify(value, null, 2)}
              </groupingComponent_1.GroupingValue>)}
          </groupingComponent_1.GroupingComponentListItem>))}
    </react_1.Fragment>);
};
exports.default = GroupingComponentChildren;
//# sourceMappingURL=groupingComponentChildren.jsx.map