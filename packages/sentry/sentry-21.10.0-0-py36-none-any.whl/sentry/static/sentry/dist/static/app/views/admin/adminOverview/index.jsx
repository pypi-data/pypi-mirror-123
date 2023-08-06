Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const apiChart_1 = (0, tslib_1.__importDefault)(require("./apiChart"));
const eventChart_1 = (0, tslib_1.__importDefault)(require("./eventChart"));
const AdminOverview = () => {
    const resolution = '1h';
    const since = new Date().getTime() / 1000 - 3600 * 24 * 7;
    return (<react_document_title_1.default title="Admin Overview - Sentry">
      <react_1.Fragment>
        <h3>{(0, locale_1.t)('System Overview')}</h3>

        <panels_1.Panel key="events">
          <panels_1.PanelHeader>{(0, locale_1.t)('Event Throughput')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <eventChart_1.default since={since} resolution={resolution}/>
          </panels_1.PanelBody>
        </panels_1.Panel>

        <panels_1.Panel key="api">
          <panels_1.PanelHeader>{(0, locale_1.t)('API Responses')}</panels_1.PanelHeader>
          <panels_1.PanelBody withPadding>
            <apiChart_1.default since={since} resolution={resolution}/>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>
    </react_document_title_1.default>);
};
exports.default = AdminOverview;
//# sourceMappingURL=index.jsx.map