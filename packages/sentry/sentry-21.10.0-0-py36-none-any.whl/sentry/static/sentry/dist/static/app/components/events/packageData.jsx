Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const clippedBox_1 = (0, tslib_1.__importDefault)(require("app/components/clippedBox"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const locale_1 = require("app/locale");
class EventPackageData extends react_1.Component {
    shouldComponentUpdate(nextProps) {
        return this.props.event.id !== nextProps.event.id;
    }
    render() {
        const { event } = this.props;
        let longKeys, title;
        const packages = Object.entries(event.packages || {}).map(([key, value]) => ({
            key,
            value,
            subject: key,
            meta: (0, metaProxy_1.getMeta)(event.packages, key),
        }));
        switch (event.platform) {
            case 'csharp':
                longKeys = true;
                title = (0, locale_1.t)('Assemblies');
                break;
            default:
                longKeys = false;
                title = (0, locale_1.t)('Packages');
        }
        return (<eventDataSection_1.default type="packages" title={title}>
        <clippedBox_1.default>
          <errorBoundary_1.default mini>
            <keyValueList_1.default data={packages} longKeys={longKeys}/>
          </errorBoundary_1.default>
        </clippedBox_1.default>
      </eventDataSection_1.default>);
    }
}
exports.default = EventPackageData;
//# sourceMappingURL=packageData.jsx.map