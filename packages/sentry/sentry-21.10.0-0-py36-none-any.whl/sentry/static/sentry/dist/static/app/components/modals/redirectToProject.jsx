Object.defineProperty(exports, "__esModule", { value: true });
exports.RedirectToProjectModal = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const text_1 = (0, tslib_1.__importDefault)(require("app/components/text"));
const locale_1 = require("app/locale");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
class RedirectToProjectModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            timer: 5,
        };
    }
    componentDidMount() {
        setInterval(() => {
            if (this.state.timer <= 1) {
                window.location.assign(this.newPath);
                return;
            }
            this.setState(state => ({
                timer: state.timer - 1,
            }));
        }, 1000);
    }
    get newPath() {
        const { params, slug } = this.props;
        return (0, recreateRoute_1.default)('', Object.assign(Object.assign({}, this.props), { params: Object.assign(Object.assign({}, params), { projectId: slug }) }));
    }
    render() {
        const { slug, Header, Body } = this.props;
        return (<react_1.Fragment>
        <Header>{(0, locale_1.t)('Redirecting to New Project...')}</Header>

        <Body>
          <div>
            <text_1.default>
              <p>{(0, locale_1.t)('The project slug has been changed.')}</p>

              <p>
                {(0, locale_1.tct)('You will be redirected to the new project [project] in [timer] seconds...', {
                project: <strong>{slug}</strong>,
                timer: `${this.state.timer}`,
            })}
              </p>
              <ButtonWrapper>
                <button_1.default priority="primary" href={this.newPath}>
                  {(0, locale_1.t)('Continue to %s', slug)}
                </button_1.default>
              </ButtonWrapper>
            </text_1.default>
          </div>
        </Body>
      </react_1.Fragment>);
    }
}
exports.RedirectToProjectModal = RedirectToProjectModal;
exports.default = (0, react_router_1.withRouter)(RedirectToProjectModal);
const ButtonWrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
`;
//# sourceMappingURL=redirectToProject.jsx.map