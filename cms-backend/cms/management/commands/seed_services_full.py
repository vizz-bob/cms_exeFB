from django.core.management.base import BaseCommand
from cms.models import Service, ServiceSubService

class Command(BaseCommand):
    help = 'Seeds the Services with complete data from the updated list'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Seeding Full Services Data...')
        
        # Clear old data to prevent duplicates
        Service.objects.all().delete()

        # Data Structure from your prompt
        services_data = [
            {
                "title": "Virtual CFO & Advisory",
                "slug": "virtual-cfo-advisory",
                "icon": "TrendingUp",
                "short_description": "Strategic financial guidance, risk management, and business restructuring.",
                "sub_services": [
                    "Virtual CFO Services",
                    "Financial Advisory Services",
                    "Treasury & Risk Management",
                    "Business Restructuring & Turnaround",
                    "ESG & Sustainable Finance Advisory"
                ]
            },
            {
                "title": "Audit & Assurance",
                "slug": "audit-assurance",
                "icon": "ShieldCheck",
                "short_description": "Comprehensive auditing services ensuring compliance and accuracy.",
                "sub_services": [
                    "Statutory & Tax Audits",
                    "Internal & Management Audits",
                    "Forensic & Fraud Audits",
                    "System and IT Audits",
                    "Risk & Process Audits",
                    "Bank, Stock & Concurrent Audits",
                    "ESG & CSR Impact Audits"
                ]
            },
            {
                "title": "Accounting & Outsourcing",
                "slug": "accounting-outsourcing",
                "icon": "Calculator",
                "short_description": "End-to-end bookkeeping and cloud accounting support.",
                "sub_services": [
                    "End-to-End Bookkeeping & Accounting",
                    "Cloud-Based Accounting (Tally, Xero, Zoho, SAP, QuickBooks)",
                    "MIS & Financial Reporting",
                    "Accounts Payable & Receivable Outsourcing",
                    "Consolidation & Multi-Entity Reporting",
                    "Virtual Back-Office Support"
                ]
            },
            {
                "title": "Payroll, HR & Recruitment",
                "slug": "payroll-hr-recruitment",
                "icon": "Users",
                "short_description": "Managing payroll compliance and talent recruitment.",
                "sub_services": [
                    "Payroll Processing & Compliance (PF, ESI, Gratuity)",
                    "Recruitment & Talent Advisory",
                    "International Payroll & HR Structuring",
                    "HR Outsourcing & Talent Recruitment",
                    "Compensation Structuring & Benefits Advisory",
                    "HR Policies, Contracts & Documentation"
                ]
            },
            {
                "title": "Taxation & Compliance",
                "slug": "taxation-compliance",
                "icon": "FileText",
                "short_description": "Expert handling of GST, Tax Returns, and International Taxation.",
                "sub_services": [
                    "Tax Advisory & Returns (Individuals & Corporates)",
                    "GST Registration, Filing & Advisory",
                    "Transfer Pricing & Cross-Border Taxation",
                    "International Tax & DTAA Advisory",
                    "FEMA, RBI, FDI, ODI Compliance",
                    "Global Minimum Tax (OECD) Compliance",
                    "Local Compliance",
                    "International Compliance",
                    "Expatriate Taxation & NRI Services"
                ]
            },
            {
                "title": "Corporate Legal & Secretarial",
                "slug": "corporate-legal",
                "icon": "Scale",
                "short_description": "Company incorporation and legal advisory services.",
                "sub_services": [
                    "Registration & Company Incorporation (Pvt, LLP, OPC, Public, Trusts, Section 8, etc.)",
                    "Other Licenses (IEC, FSSAI, RERA, Trade License, etc.)",
                    "Corporate Governance & ROC Filings",
                    "M&A, Corporate Restructuring & Valuations",
                    "Due Diligence & Legal Compliance",
                    "Insolvency & Bankruptcy Advisory",
                    "Contract Drafting & Legal Advisory"
                ]
            },
            {
                "title": "Fundraising & Capital Advisory",
                "slug": "fundraising-capital",
                "icon": "Coins",
                "short_description": "Support for fundraising, IPO advisory, and project finance.",
                "sub_services": [
                    "Startup Fundraising (Seed, Angel, VC, PE)",
                    "Financial Modelling & Business Valuation",
                    "Pitch Decks & Investor Readiness",
                    "Debt Syndication & Project Finance",
                    "IPO & SME IPO Advisory",
                    "Incubation Services",
                    "Retail Loans"
                ]
            },
            {
                "title": "Wealth & Investment Advisory",
                "slug": "wealth-investment",
                "icon": "PieChart",
                "short_description": "Portfolio management and estate planning.",
                "sub_services": [
                    "Wealth & Portfolio Management",
                    "Mutual Funds, Equities & Alternative Investments",
                    "Real Estate Advisory & Transaction Support",
                    "Retail Loans (Home, Business, Vehicle, Personal)",
                    "Insurance & Risk Advisory",
                    "Succession & Estate Planning"
                ]
            },
            {
                "title": "Startup & Incubation Support",
                "slug": "startup-incubation",
                "icon": "Rocket",
                "short_description": "End-to-end support for startups from incorporation to exit.",
                "sub_services": [
                    "Startup Incorporation & Compliance",
                    "Virtual CFO for Startups",
                    "Growth Strategy & Business Planning",
                    "Pitch Preparation & Investor Access",
                    "Mentorship & Networking",
                    "Technology & Automation Support"
                ]
            },
            {
                "title": "Tech-Enabled Solutions",
                "slug": "tech-solutions",
                "icon": "Cpu",
                "short_description": "AI, Blockchain, and RPA tools for financial automation.",
                "sub_services": [
                    "AI-Powered Accounting Tools",
                    "Blockchain based Audit & Compliance",
                    "RPA-Driven Automation in Finance",
                    "Data Analytics, Forecasting & BI Dashboard",
                    "ERP / FinTech Integration (SAP, Zoho, Tally, Oracle, Microsoft)",
                    "Digital Transformation Advisory"
                ]
            }
        ]

        for service_data in services_data:
            # Create Main Service
            service = Service.objects.create(
                title=service_data['title'],
                slug=service_data['slug'],
                icon=service_data['icon'],
                short_description=service_data['short_description'],
                full_description="Explore our specialized offerings in this domain."
            )
            
            # Create Sub-Services
            for index, sub_title in enumerate(service_data['sub_services']):
                ServiceSubService.objects.create(
                    service=service,
                    title=sub_title,
                    description=f"Detailed service for {sub_title}",
                    order=index + 1
                )
            
            self.stdout.write(f"   ✅ Created Service: {service.title} with {len(service_data['sub_services'])} sub-points")

        self.stdout.write(self.style.SUCCESS('\n🎉 All Services & Detailed Sub-points Seeded Successfully!'))