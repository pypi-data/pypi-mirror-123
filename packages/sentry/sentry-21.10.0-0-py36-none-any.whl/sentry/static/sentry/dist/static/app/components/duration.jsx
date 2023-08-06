Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const formatters_1 = require("app/utils/formatters");
const Duration = (_a) => {
    var { seconds, fixedDigits, abbreviation, exact } = _a, props = (0, tslib_1.__rest)(_a, ["seconds", "fixedDigits", "abbreviation", "exact"]);
    return (<span {...props}>
    {exact
            ? (0, formatters_1.getExactDuration)(seconds, abbreviation)
            : (0, formatters_1.getDuration)(seconds, fixedDigits, abbreviation)}
  </span>);
};
exports.default = Duration;
//# sourceMappingURL=duration.jsx.map