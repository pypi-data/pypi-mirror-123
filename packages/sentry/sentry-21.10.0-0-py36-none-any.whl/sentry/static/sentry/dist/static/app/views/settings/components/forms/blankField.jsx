Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
/**
 * This class is meant to hook into `fieldFromConfig`. Like the FieldSeparator
 * class, this doesn't have any fields of its own and is just meant to make
 * forms more flexible.
 */
class BlankField extends React.Component {
    render() {
        return <field_1.default {...this.props}/>;
    }
}
exports.default = BlankField;
//# sourceMappingURL=blankField.jsx.map