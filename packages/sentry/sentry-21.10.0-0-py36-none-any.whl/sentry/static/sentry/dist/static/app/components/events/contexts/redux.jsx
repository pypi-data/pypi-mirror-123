Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const clippedBox_1 = (0, tslib_1.__importDefault)(require("app/components/clippedBox"));
const contextBlock_1 = (0, tslib_1.__importDefault)(require("app/components/events/contexts/contextBlock"));
const locale_1 = require("app/locale");
class ReduxContextType extends React.Component {
    getKnownData() {
        return [
            {
                key: 'value',
                subject: (0, locale_1.t)('Latest State'),
                value: this.props.data,
            },
        ];
    }
    render() {
        return (<clippedBox_1.default clipHeight={250}>
        <contextBlock_1.default data={this.getKnownData()}/>
      </clippedBox_1.default>);
    }
}
exports.default = ReduxContextType;
//# sourceMappingURL=redux.jsx.map