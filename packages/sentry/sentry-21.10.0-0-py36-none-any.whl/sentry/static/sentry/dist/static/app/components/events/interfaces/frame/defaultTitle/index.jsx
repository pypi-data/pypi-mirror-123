Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const stacktracePreview_1 = require("app/components/stacktracePreview");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const truncate_1 = (0, tslib_1.__importDefault)(require("app/components/truncate"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const functionName_1 = (0, tslib_1.__importDefault)(require("../functionName"));
const groupingIndicator_1 = (0, tslib_1.__importDefault)(require("../groupingIndicator"));
const utils_2 = require("../utils");
const originalSourceInfo_1 = (0, tslib_1.__importDefault)(require("./originalSourceInfo"));
const DefaultTitle = ({ frame, platform, isHoverPreviewed, isUsedForGrouping }) => {
    const title = [];
    const framePlatform = (0, utils_2.getPlatform)(frame.platform, platform);
    const tooltipDelay = isHoverPreviewed ? stacktracePreview_1.STACKTRACE_PREVIEW_TOOLTIP_DELAY : undefined;
    const handleExternalLink = (event) => {
        event.stopPropagation();
    };
    const getModule = () => {
        if (frame.module) {
            return {
                key: 'module',
                value: frame.module,
                meta: (0, metaProxy_1.getMeta)(frame, 'module'),
            };
        }
        return undefined;
    };
    const getPathNameOrModule = (shouldPrioritizeModuleName) => {
        if (shouldPrioritizeModuleName) {
            if (frame.module) {
                return getModule();
            }
            if (frame.filename) {
                return {
                    key: 'filename',
                    value: frame.filename,
                    meta: (0, metaProxy_1.getMeta)(frame, 'filename'),
                };
            }
            return undefined;
        }
        if (frame.filename) {
            return {
                key: 'filename',
                value: frame.filename,
                meta: (0, metaProxy_1.getMeta)(frame, 'filename'),
            };
        }
        if (frame.module) {
            return getModule();
        }
        return undefined;
    };
    // TODO(dcramer): this needs to use a formatted string so it can be
    // localized correctly
    if ((0, utils_1.defined)(frame.filename || frame.module)) {
        // prioritize module name for Java as filename is often only basename
        const shouldPrioritizeModuleName = framePlatform === 'java';
        // we do not want to show path in title on csharp platform
        const pathNameOrModule = (0, utils_2.isDotnet)(framePlatform)
            ? getModule()
            : getPathNameOrModule(shouldPrioritizeModuleName);
        const enablePathTooltip = (0, utils_1.defined)(frame.absPath) && frame.absPath !== (pathNameOrModule === null || pathNameOrModule === void 0 ? void 0 : pathNameOrModule.value);
        if (pathNameOrModule) {
            title.push(<tooltip_1.default key={pathNameOrModule.key} title={frame.absPath} disabled={!enablePathTooltip} delay={tooltipDelay}>
          <code key="filename" className="filename" data-test-id="filename">
            <annotatedText_1.default value={<truncate_1.default value={pathNameOrModule.value} maxLength={100} leftTrim/>} meta={pathNameOrModule.meta}/>
          </code>
        </tooltip_1.default>);
        }
        // in case we prioritized the module name but we also have a filename info
        // we want to show a litle (?) icon that on hover shows the actual filename
        if (shouldPrioritizeModuleName && frame.filename) {
            title.push(<tooltip_1.default key={frame.filename} title={frame.filename} delay={tooltipDelay}>
          <a className="in-at real-filename">
            <icons_1.IconQuestion size="xs"/>
          </a>
        </tooltip_1.default>);
        }
        if (frame.absPath && (0, utils_1.isUrl)(frame.absPath)) {
            title.push(<StyledExternalLink href={frame.absPath} key="share" onClick={handleExternalLink}>
          <icons_1.IconOpen size="xs"/>
        </StyledExternalLink>);
        }
        if (((0, utils_1.defined)(frame.function) || (0, utils_1.defined)(frame.rawFunction)) &&
            (0, utils_1.defined)(pathNameOrModule)) {
            title.push(<InFramePosition className="in-at" key="in">
          {` ${(0, locale_1.t)('in')} `}
        </InFramePosition>);
        }
    }
    if ((0, utils_1.defined)(frame.function) || (0, utils_1.defined)(frame.rawFunction)) {
        title.push(<functionName_1.default frame={frame} key="function" className="function" data-test-id="function"/>);
    }
    // we don't want to render out zero line numbers which are used to
    // indicate lack of source information for native setups.  We could
    // TODO(mitsuhiko): only do this for events from native platforms?
    if ((0, utils_1.defined)(frame.lineNo) && frame.lineNo !== 0) {
        title.push(<InFramePosition className="in-at in-at-line" key="no">
        {` ${(0, locale_1.t)('at line')} `}
      </InFramePosition>);
        title.push(<code key="line" className="lineno">
        {(0, utils_1.defined)(frame.colNo) ? `${frame.lineNo}:${frame.colNo}` : frame.lineNo}
      </code>);
    }
    if ((0, utils_1.defined)(frame.package) && !(0, utils_2.isDotnet)(framePlatform)) {
        title.push(<InFramePosition key="within">{` ${(0, locale_1.t)('within')} `}</InFramePosition>);
        title.push(<code title={frame.package} className="package" key="package">
        {(0, utils_2.trimPackage)(frame.package)}
      </code>);
    }
    if ((0, utils_1.defined)(frame.origAbsPath)) {
        title.push(<tooltip_1.default key="info-tooltip" title={<originalSourceInfo_1.default mapUrl={frame.mapUrl} map={frame.map}/>} delay={tooltipDelay}>
        <a className="in-at original-src">
          <icons_1.IconQuestion size="xs"/>
        </a>
      </tooltip_1.default>);
    }
    if (isUsedForGrouping) {
        title.push(<StyledGroupingIndicator key="info-tooltip"/>);
    }
    return <React.Fragment>{title}</React.Fragment>;
};
exports.default = DefaultTitle;
const StyledExternalLink = (0, styled_1.default)(externalLink_1.default) `
  position: relative;
  top: ${(0, space_1.default)(0.25)};
  margin-left: ${(0, space_1.default)(0.5)};
`;
const InFramePosition = (0, styled_1.default)('span') `
  color: ${p => p.theme.textColor};
  opacity: 0.6;
`;
const StyledGroupingIndicator = (0, styled_1.default)(groupingIndicator_1.default) `
  margin-left: ${(0, space_1.default)(0.75)};
`;
//# sourceMappingURL=index.jsx.map