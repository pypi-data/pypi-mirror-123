Object.defineProperty(exports, "__esModule", { value: true });
exports.ErrorRobot = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const sentry_robot_png_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/sentry-robot.png"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const createSampleEventButton_1 = (0, tslib_1.__importDefault)(require("app/views/onboarding/createSampleEventButton"));
class ErrorRobot extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            error: false,
            loading: false,
            sampleIssueId: this.props.sampleIssueId,
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    fetchData() {
        var _a, _b;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { org, project } = this.props;
            const { sampleIssueId } = this.state;
            if (!project) {
                return;
            }
            if ((0, utils_1.defined)(sampleIssueId)) {
                return;
            }
            const url = `/projects/${org.slug}/${project.slug}/issues/`;
            this.setState({ loading: true });
            try {
                const data = yield this.props.api.requestPromise(url, {
                    method: 'GET',
                    data: { limit: 1 },
                });
                this.setState({ sampleIssueId: (data.length > 0 && data[0].id) || '' });
            }
            catch (err) {
                const error = (_b = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : true;
                this.setState({ error });
            }
            this.setState({ loading: false });
        });
    }
    render() {
        const { loading, error, sampleIssueId } = this.state;
        const { org, project, gradient } = this.props;
        const sampleLink = project && (loading || error ? null : sampleIssueId) ? (<p>
          <link_1.default to={`/${org.slug}/${project.slug}/issues/${sampleIssueId}/?sample`}>
            {(0, locale_1.t)('Or see your sample event')}
          </link_1.default>
        </p>) : (<p>
          <createSampleEventButton_1.default priority="link" project={project} source="issues_list" disabled={!project} title={!project ? (0, locale_1.t)('Select a project to create a sample event') : undefined}>
            {(0, locale_1.t)('Create a sample event')}
          </createSampleEventButton_1.default>
        </p>);
        return (<ErrorRobotWrapper data-test-id="awaiting-events" className="awaiting-events" gradient={gradient}>
        <Robot aria-hidden>
          <Eye />
        </Robot>
        <MessageContainer>
          <h3>{(0, locale_1.t)('Waiting for events…')}</h3>
          <p>
            {(0, locale_1.tct)('Our error robot is waiting to [strike:devour] receive your first event.', {
                strike: <Strikethrough />,
            })}
          </p>
          <p>
            {project && (<button_1.default data-test-id="install-instructions" priority="primary" to={`/${org.slug}/${project.slug}/getting-started/${project.platform || ''}`}>
                {(0, locale_1.t)('Installation Instructions')}
              </button_1.default>)}
          </p>
          {sampleLink}
        </MessageContainer>
      </ErrorRobotWrapper>);
    }
}
exports.ErrorRobot = ErrorRobot;
exports.default = (0, withApi_1.default)(ErrorRobot);
const ErrorRobotWrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
  font-size: ${p => p.theme.fontSizeExtraLarge};
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.08);
  border-radius: 0 0 3px 3px;
  padding: 40px ${(0, space_1.default)(3)} ${(0, space_1.default)(3)};
  min-height: 260px;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    flex-direction: column;
    align-items: center;
    padding: ${(0, space_1.default)(3)};
    text-align: center;
  }
`;
const Robot = (0, styled_1.default)('div') `
  display: block;
  position: relative;
  width: 220px;
  height: 260px;
  background: url(${sentry_robot_png_1.default});
  background-size: cover;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    width: 110px;
    height: 130px;
  }
`;
const Eye = (0, styled_1.default)('span') `
  width: 12px;
  height: 12px;
  border-radius: 50%;
  position: absolute;
  top: 70px;
  left: 81px;
  transform: translateZ(0);
  animation: blink-eye 0.6s infinite;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    width: 6px;
    height: 6px;
    top: 35px;
    left: 41px;
  }

  @keyframes blink-eye {
    0% {
      background: #e03e2f;
      box-shadow: 0 0 10px #e03e2f;
    }

    50% {
      background: #4a4d67;
      box-shadow: none;
    }

    100% {
      background: #e03e2f;
      box-shadow: 0 0 10px #e03e2f;
    }
  }
`;
const MessageContainer = (0, styled_1.default)('div') `
  align-self: center;
  max-width: 480px;
  margin-left: 40px;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    margin: 0;
  }
`;
const Strikethrough = (0, styled_1.default)('span') `
  text-decoration: line-through;
`;
//# sourceMappingURL=errorRobot.jsx.map