Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const startCase_1 = (0, tslib_1.__importDefault)(require("lodash/startCase"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const eventErrors_1 = require("app/constants/eventErrors");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("../links/externalLink"));
const keyMapping = {
    image_uuid: 'Debug ID',
    image_name: 'File Name',
    image_path: 'File Path',
};
class ErrorItem extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isOpen: false,
        };
        this.handleToggle = () => {
            this.setState({ isOpen: !this.state.isOpen });
        };
    }
    shouldComponentUpdate(_nextProps, nextState) {
        return this.state.isOpen !== nextState.isOpen;
    }
    cleanedData(errorData) {
        const data = Object.assign({}, errorData);
        // The name is rendered as path in front of the message
        if (typeof data.name === 'string') {
            delete data.name;
        }
        if (data.message === 'None') {
            // Python ensures a message string, but "None" doesn't make sense here
            delete data.message;
        }
        if (typeof data.image_path === 'string') {
            // Separate the image name for readability
            const separator = /^([a-z]:\\|\\\\)/i.test(data.image_path) ? '\\' : '/';
            const path = data.image_path.split(separator);
            data.image_name = path.splice(-1, 1)[0];
            data.image_path = path.length ? path.join(separator) + separator : '';
        }
        if (typeof data.server_time === 'string' && typeof data.sdk_time === 'string') {
            data.message = (0, locale_1.t)('Adjusted timestamps by %s', moment_1.default
                .duration(moment_1.default.utc(data.server_time).diff(moment_1.default.utc(data.sdk_time)))
                .humanize());
        }
        return Object.entries(data).map(([key, value]) => ({
            key,
            value,
            subject: keyMapping[key] || (0, startCase_1.default)(key),
            meta: (0, metaProxy_1.getMeta)(data, key),
        }));
    }
    renderPath(data) {
        const { name } = data;
        if (!name || typeof name !== 'string') {
            return null;
        }
        return (<React.Fragment>
        <strong>{name}</strong>
        {': '}
      </React.Fragment>);
    }
    renderTroubleshootingLink(error) {
        if (Object.values(eventErrors_1.JavascriptProcessingErrors).includes(error.type)) {
            return (<React.Fragment>
          {' '}
          (
          {(0, locale_1.tct)('see [docsLink]', {
                    docsLink: (<StyledExternalLink href="https://docs.sentry.io/platforms/javascript/sourcemaps/troubleshooting_js/">
                {(0, locale_1.t)('Troubleshooting for JavaScript')}
              </StyledExternalLink>),
                })}
          )
        </React.Fragment>);
        }
        return null;
    }
    render() {
        var _a;
        const { error } = this.props;
        const { isOpen } = this.state;
        const data = (_a = error === null || error === void 0 ? void 0 : error.data) !== null && _a !== void 0 ? _a : {};
        const cleanedData = this.cleanedData(data);
        return (<StyledListItem>
        <OverallInfo>
          <div>
            {this.renderPath(data)}
            {error.message}
            {this.renderTroubleshootingLink(error)}
          </div>
          {!!cleanedData.length && (<ToggleButton onClick={this.handleToggle} priority="link">
              {isOpen ? (0, locale_1.t)('Collapse') : (0, locale_1.t)('Expand')}
            </ToggleButton>)}
        </OverallInfo>
        {isOpen && <keyValueList_1.default data={cleanedData} isContextData/>}
      </StyledListItem>);
    }
}
exports.default = ErrorItem;
const ToggleButton = (0, styled_1.default)(button_1.default) `
  margin-left: ${(0, space_1.default)(1.5)};
  font-weight: 700;
  color: ${p => p.theme.subText};
  :hover,
  :focus {
    color: ${p => p.theme.textColor};
  }
`;
const StyledListItem = (0, styled_1.default)(listItem_1.default) `
  margin-bottom: ${(0, space_1.default)(0.75)};
`;
const StyledExternalLink = (0, styled_1.default)(externalLink_1.default) `
  /* && is here to increase specificity to override default styles*/
  && {
    font-weight: inherit;
    color: inherit;
    text-decoration: underline;
  }
`;
const OverallInfo = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: repeat(2, minmax(auto, max-content));
  word-break: break-all;
`;
//# sourceMappingURL=errorItem.jsx.map