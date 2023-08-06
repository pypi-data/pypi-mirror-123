Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
function openFeedback(e) {
    e.preventDefault();
    Sentry.showReportDialog();
}
class DetailedError extends React.Component {
    componentDidMount() {
        // XXX(epurkhiser): Why is this here?
        setTimeout(() => this.forceUpdate(), 100);
    }
    render() {
        const { className, heading, message, onRetry, hideSupportLinks } = this.props;
        const cx = (0, classnames_1.default)('detailed-error', className);
        const showFooter = !!onRetry || !hideSupportLinks;
        return (<div className={cx}>
        <div className="detailed-error-icon">
          <icons_1.IconFlag size="lg"/>
        </div>
        <div className="detailed-error-content">
          <h4>{heading}</h4>

          <div className="detailed-error-content-body">{message}</div>

          {showFooter && (<div className="detailed-error-content-footer">
              <div>
                {onRetry && (<a onClick={onRetry} className="btn btn-default">
                    {(0, locale_1.t)('Retry')}
                  </a>)}
              </div>

              {!hideSupportLinks && (<div className="detailed-error-support-links">
                  {Sentry.lastEventId() && (<button_1.default priority="link" onClick={openFeedback}>
                      {(0, locale_1.t)('Fill out a report')}
                    </button_1.default>)}
                  <a href="https://status.sentry.io/">{(0, locale_1.t)('Service status')}</a>

                  <a href="https://sentry.io/support/">{(0, locale_1.t)('Contact support')}</a>
                </div>)}
            </div>)}
        </div>
      </div>);
    }
}
DetailedError.defaultProps = {
    hideSupportLinks: false,
};
exports.default = DetailedError;
//# sourceMappingURL=detailedError.jsx.map