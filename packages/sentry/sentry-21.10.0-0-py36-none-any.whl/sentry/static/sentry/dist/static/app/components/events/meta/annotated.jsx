Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const metaData_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/metaData"));
const utils_1 = require("app/utils");
/**
 * Returns the value of `object[prop]` and returns an annotated component if
 * there is meta data
 */
const Annotated = ({ children, object, objectKey, required = false, }) => {
    return (<metaData_1.default object={object} prop={objectKey} required={required}>
      {(value, meta) => {
            const toBeReturned = <annotatedText_1.default value={value} meta={meta}/>;
            return (0, utils_1.isFunction)(children) ? children(toBeReturned) : toBeReturned;
        }}
    </metaData_1.default>);
};
exports.default = Annotated;
//# sourceMappingURL=annotated.jsx.map