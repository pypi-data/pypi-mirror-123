Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const constants_1 = require("app/constants");
const selectorItem_1 = (0, tslib_1.__importDefault)(require("./selectorItem"));
const RelativeSelector = ({ onClick, selected, relativePeriods }) => (<React.Fragment>
    {Object.entries(relativePeriods || constants_1.DEFAULT_RELATIVE_PERIODS).map(([value, label]) => (<selectorItem_1.default key={value} onClick={onClick} value={value} label={label} selected={selected === value}/>))}
  </React.Fragment>);
exports.default = RelativeSelector;
//# sourceMappingURL=relativeSelector.jsx.map