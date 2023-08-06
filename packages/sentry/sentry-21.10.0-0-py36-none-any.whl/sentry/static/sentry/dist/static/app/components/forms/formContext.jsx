Object.defineProperty(exports, "__esModule", { value: true });
const react_1 = require("react");
/**
 * Default to undefined to preserve backwards compatibility.
 * The FormField component uses a truthy test to see if it is connected
 * to context or if the control is 'uncontrolled'.
 */
const FormContext = (0, react_1.createContext)({});
exports.default = FormContext;
//# sourceMappingURL=formContext.jsx.map