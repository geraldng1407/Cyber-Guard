import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';
import clientSsoGatewayLogo from '../logos/client-sso-gateway.png';
import complianceMonitoringToolLogo from '../logos/compliance-monitoring-tool.png';
import corporateTreasuryManagementLogo from '../logos/corporate-treasury-management-system.png';
import crmPortalLogo from '../logos/crm-portal.png';
import customerInfoDatabaseLogo from '../logos/customer-information-database.png';
import documentWorkflowManagerLogo from '../logos/document-workflow-manager.png';
import identityAccessManagerLogo from '../logos/identity-access-manager.png';
import marketDataAggregatorLogo from '../logos/market-data-aggregator.png';
import marketMonitoringInterfaceLogo from '../logos/market-monitoring-interface.png';
import mfaSystemLogo from '../logos/multi-factor-authentication-system.png';
import paymentProcessingLogo from '../logos/payment-processing.png';
import portfolioManagementDashboardLogo from '../logos/portfolio-management-dashboard.png';
import retailBankingPortalLogo from '../logos/retail-banking-portal.png';
import riskCalculationEngineLogo from '../logos/risk-calculation-engine.png';
import riskDataWarehouseLogo from '../logos/risk-data-warehouse.png';
import taskSchedulingSystemLogo from '../logos/task-scheduling-system.png';
import tradeExecutionPlatformLogo from '../logos/trade-execution-platform.png';
import tradeRepositoryLogo from '../logos/trade-repository.png';

export default function ApplicationDetails() {
  const { app_id } = useParams();
  const [appDetails, setAppDetails] = useState({
    name: "",
    versionNumber: "",
    provider: "",
    releaseDate: "",
    buildNumber: "",
    runningInstances: [],
    description: ""
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const appLogos = {
    1: paymentProcessingLogo,
    2: marketDataAggregatorLogo,
    3: riskCalculationEngineLogo,
    4: portfolioManagementDashboardLogo,
    5: marketMonitoringInterfaceLogo,
    6: crmPortalLogo,
    7: retailBankingPortalLogo,
    8: corporateTreasuryManagementLogo,
    9: tradeExecutionPlatformLogo,
    10: identityAccessManagerLogo,
    11: mfaSystemLogo,
    12: clientSsoGatewayLogo,
    13: customerInfoDatabaseLogo,
    14: tradeRepositoryLogo,
    15: riskDataWarehouseLogo,
    16: documentWorkflowManagerLogo,
    17: taskSchedulingSystemLogo,
    18: complianceMonitoringToolLogo,
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:8088//applications/${app_id}`);
        if (!response.ok) {
          throw new Error(`Error: ${response.statusText}`);
        }
        const data = await response.json();
  
        const firstInstance = data[0];
        setAppDetails({
          name: firstInstance.app_name,
          versionNumber: firstInstance.version_no,
          provider: firstInstance.provider,
          releaseDate: new Date(firstInstance.release_date).toLocaleDateString(),
          buildNumber: firstInstance.build_no,
          runningInstances: data,
          description: firstInstance.description
        });
        console.log(appDetails)
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="min-h-screen bg-[#0D0D2B] text-white p-8">
      {/* Application Details Panel */}
      <section className="h-1/2 mb-8 flex">
        <div className="w-1/3 flex flex-col justify-between p-6">
          <h2 className="text-4xl font-bold">{appDetails.name}</h2>
          <div className="flex justify-center">
            <img 
              src={appLogos[app_id]} 
              alt={`${appDetails.name} Logo`} 
              style={{ maxWidth: '125px', maxHeight: '125px', objectFit: 'contain' }} 
            />
          </div>
        </div>

        <div className="w-[2px] bg-gray-500 mx-4"></div>

        <div className="w-2/3 bg-gray-800 p-6 rounded-lg shadow-md">
          <div className="grid grid-cols-1 gap-4">
            <div>
              <p><strong>VERSION NUMBER:</strong> {appDetails.versionNumber}</p>
              <p><strong>PROVIDER:</strong> {appDetails.provider}</p>
              <p><strong>RELEASE DATE:</strong> {appDetails.releaseDate}</p>
              <p><strong>BUILD NUMBER:</strong> {appDetails.buildNumber}</p>
              <p><strong>NUMBER OF RUNNING INSTANCES:</strong> {appDetails.runningInstances.length}</p>
            </div>
            <div className="bg-[#001F3F] p-4 rounded-lg">
              <p>
                {appDetails.description}
              </p>
            </div>
          </div>
        </div>
      </section>

      <div className="h-1/2">
        <section className="bg-gray-800 p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4">RUNNING INSTANCES</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-white">
              <thead className="bg-[#000230]">
                <tr>
                  <th className="px-6 py-2">Instance ID</th>
                  <th className="px-6 py-2">Location</th>
                  <th className="px-6 py-2">Instance Name</th>
                  <th className="px-6 py-2">Country Code</th>
                </tr>
              </thead>
              <tbody className="bg-[#000230]">
                {appDetails.runningInstances.map((instance) => (
                  <tr 
                    key={instance.instance_id}
                    className="border-t border-gray-700 hover:bg-[#001F3F] cursor-pointer transition duration-200"
                    onClick={() => window.location.href = `/instance/${instance.instance_id}`}
                  >
                    <td className="px-6 py-4">{instance.instance_id}</td>
                    <td className="px-6 py-4">{instance.country}</td>
                    <td className="px-6 py-4">{instance.instance_name}</td>
                    <td className="px-6 py-4">{instance.code}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}
