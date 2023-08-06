Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const upperFirst_1 = (0, tslib_1.__importDefault)(require("lodash/upperFirst"));
const clippedBox_1 = (0, tslib_1.__importDefault)(require("app/components/clippedBox"));
const contextBlock_1 = (0, tslib_1.__importDefault)(require("app/components/events/contexts/contextBlock"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const locale_1 = require("app/locale");
class StateContextType extends React.Component {
    getStateTitle(name, type) {
        return `${name}${type ? ` (${(0, upperFirst_1.default)(type)})` : ''}`;
    }
    getKnownData() {
        const primaryState = this.props.data.state;
        if (!primaryState) {
            return [];
        }
        return [
            {
                key: 'state',
                subject: this.getStateTitle((0, locale_1.t)('State'), primaryState.type),
                value: primaryState.value,
            },
        ];
    }
    getUnknownData() {
        const { data } = this.props;
        return Object.entries(data)
            .filter(([key]) => !['type', 'title', 'state'].includes(key))
            .map(([name, state]) => ({
            key: name,
            value: state.value,
            subject: this.getStateTitle(name, state.type),
            meta: (0, metaProxy_1.getMeta)(data, name),
        }));
    }
    render() {
        return (<clippedBox_1.default clipHeight={250}>
        <contextBlock_1.default data={this.getKnownData()}/>
        <contextBlock_1.default data={this.getUnknownData()}/>
      </clippedBox_1.default>);
    }
}
exports.default = StateContextType;
//# sourceMappingURL=state.jsx.map