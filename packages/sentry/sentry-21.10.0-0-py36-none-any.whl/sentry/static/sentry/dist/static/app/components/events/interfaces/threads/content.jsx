Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isNil_1 = (0, tslib_1.__importDefault)(require("lodash/isNil"));
const crashContent_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/crashContent"));
const pill_1 = (0, tslib_1.__importDefault)(require("app/components/pill"));
const pills_1 = (0, tslib_1.__importDefault)(require("app/components/pills"));
const locale_1 = require("app/locale");
const noStackTraceMessage_1 = (0, tslib_1.__importDefault)(require("../noStackTraceMessage"));
const Content = ({ event, projectId, data, stackView, groupingCurrentLevel, stackType, newestFirst, exception, stacktrace, stackTraceNotFound, hasHierarchicalGrouping, }) => {
    var _a;
    return (<div className="thread">
    {data && (!(0, isNil_1.default)(data === null || data === void 0 ? void 0 : data.id) || !!(data === null || data === void 0 ? void 0 : data.name)) && (<pills_1.default>
        {!(0, isNil_1.default)(data.id) && <pill_1.default name={(0, locale_1.t)('id')} value={String(data.id)}/>}
        {!!((_a = data.name) === null || _a === void 0 ? void 0 : _a.trim()) && <pill_1.default name={(0, locale_1.t)('name')} value={data.name}/>}
        <pill_1.default name={(0, locale_1.t)('was active')} value={data.current}/>
        <pill_1.default name={(0, locale_1.t)('errored')} className={data.crashed ? 'false' : 'true'}>
          {data.crashed ? (0, locale_1.t)('yes') : (0, locale_1.t)('no')}
        </pill_1.default>
      </pills_1.default>)}

    {stackTraceNotFound ? (<noStackTraceMessage_1.default message={(data === null || data === void 0 ? void 0 : data.crashed) ? (0, locale_1.t)('Thread Errored') : undefined}/>) : (<crashContent_1.default event={event} stackType={stackType} stackView={stackView} newestFirst={newestFirst} projectId={projectId} exception={exception} stacktrace={stacktrace} groupingCurrentLevel={groupingCurrentLevel} hasHierarchicalGrouping={hasHierarchicalGrouping}/>)}
  </div>);
};
exports.default = Content;
//# sourceMappingURL=content.jsx.map