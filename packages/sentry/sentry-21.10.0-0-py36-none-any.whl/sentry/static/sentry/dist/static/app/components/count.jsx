Object.defineProperty(exports, "__esModule", { value: true });
const formatters_1 = require("app/utils/formatters");
function Count(props) {
    const { value, className } = props;
    return (<span className={className} title={value.toLocaleString()}>
      {(0, formatters_1.formatAbbreviatedNumber)(value)}
    </span>);
}
exports.default = Count;
//# sourceMappingURL=count.jsx.map