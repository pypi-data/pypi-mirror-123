Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const locale_1 = require("app/locale");
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
class AdminPackages extends asyncView_1.default {
    getEndpoints() {
        return [['data', '/internal/packages/']];
    }
    renderBody() {
        const { data } = this.state;
        const { extensions, modules } = data;
        return (<div>
        <h3>{(0, locale_1.t)('Extensions')}</h3>

        {extensions.length > 0 ? (<dl className="vars">
            {extensions.map(([key, value]) => (<react_1.Fragment key={key}>
                <dt>{key}</dt>
                <dd>
                  <pre className="val">{value}</pre>
                </dd>
              </react_1.Fragment>))}
          </dl>) : (<p>{(0, locale_1.t)('No extensions registered')}</p>)}

        <h3>{(0, locale_1.t)('Modules')}</h3>

        {modules.length > 0 ? (<dl className="vars">
            {modules.map(([key, value]) => (<react_1.Fragment key={key}>
                <dt>{key}</dt>
                <dd>
                  <pre className="val">{value}</pre>
                </dd>
              </react_1.Fragment>))}
          </dl>) : (<p>{(0, locale_1.t)('No modules registered')}</p>)}
      </div>);
    }
}
exports.default = AdminPackages;
//# sourceMappingURL=adminPackages.jsx.map