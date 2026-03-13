from django.core.management.base import BaseCommand
from legal.models import LegalPage, LegalPageSection

class Command(BaseCommand):
    help = "Seeds the database with comprehensive Legal Pages (15+ points each)"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding comprehensive legal data...")

        # ==========================================
        # 1. PRIVACY POLICY (17 Sections)
        # ==========================================
        self.create_page(
            title="Privacy Policy",
            slug="privacy-policy",
            description="We are committed to protecting your personal information and your right to privacy.",
            sections=[
                {"heading": "1. Introduction", "content": "Welcome to XpertAI Global. We respect your privacy and are committed to protecting your personal data. This privacy policy will inform you as to how we look after your personal data when you visit our website and tell you about your privacy rights and how the law protects you."},
                {"heading": "2. Information We Collect", "content": "We may collect, use, store and transfer different kinds of personal data about you which we have grouped together as Identity Data, Contact Data, Financial Data, and Technical Data."},
                {"heading": "3. How We Collect Data", "content": "We use different methods to collect data from and about you including through direct interactions (filling forms) and automated technologies or interactions (cookies)."},
                {"heading": "4. Purpose of Collection", "content": "We collect your data to register you as a new customer, process your orders, manage our relationship with you, and improve our website, products/services, marketing or customer relationships."},
                {"heading": "5. Cookies and Tracking", "content": "We use cookies and similar tracking technologies to track the activity on our Service and hold certain information. You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent."},
                {"heading": "6. Third-Party Disclosure", "content": "We do not sell, trade, or otherwise transfer to outside parties your Personally Identifiable Information unless we provide users with advance notice. This does not include website hosting partners and other parties who assist us in operating our website."},
                {"heading": "7. Data Security", "content": "We have put in place appropriate security measures to prevent your personal data from being accidentally lost, used or accessed in an unauthorized way, altered or disclosed."},
                {"heading": "8. Data Retention", "content": "We will only retain your personal data for as long as necessary to fulfil the purposes we collected it for, including for the purposes of satisfying any legal, accounting, or reporting requirements."},
                {"heading": "9. Your Legal Rights", "content": "Under certain circumstances, you have rights under data protection laws in relation to your personal data, including the right to request access, correction, erasure, restriction, transfer, or to object to processing."},
                {"heading": "10. Children's Privacy", "content": "Our Service does not address anyone under the age of 13. We do not knowingly collect personally identifiable information from anyone under the age of 13."},
                {"heading": "11. Changes to This Policy", "content": "We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the 'Last Updated' date."},
                {"heading": "12. Contact Information", "content": "If you have any questions about this Privacy Policy, please contact us via email at support@xpertai.global or through our Contact page."},
                {"heading": "13. International Transfers", "content": "Your information, including Personal Data, may be transferred to — and maintained on — computers located outside of your state, province, country or other governmental jurisdiction where the data protection laws may differ."},
                {"heading": "14. Analytics", "content": "We may use third-party Service Providers to monitor and analyze the use of our Service, such as Google Analytics."},
                {"heading": "15. Advertising Partners", "content": "We may work with advertisers who use cookies and similar technologies to provide you with more relevant advertising on our site and across the internet."},
                {"heading": "16. Compliance with Laws", "content": "We will disclose your Personal Data where required to do so by law or subpoena or if we believe that such action is necessary to comply with the law and the reasonable requests of law enforcement."},
                {"heading": "17. Consent", "content": "By using our website, you hereby consent to our Privacy Policy and agree to its terms."}
            ]
        )

        # ==========================================
        # 2. TERMS AND CONDITIONS (16 Sections)
        # ==========================================
        self.create_page(
            title="Terms and Conditions",
            slug="terms-and-conditions",
            description="These terms and conditions outline the rules and regulations for the use of XpertAI Global's Website.",
            sections=[
                {"heading": "1. Introduction", "content": "By accessing this website we assume you accept these terms and conditions. Do not continue to use XpertAI Global if you do not agree to take all of the terms and conditions stated on this page."},
                {"heading": "2. Intellectual Property Rights", "content": "Other than the content you own, under these Terms, XpertAI Global and/or its licensors own all the intellectual property rights and materials contained in this Website."},
                {"heading": "3. Restrictions", "content": "You are specifically restricted from publishing any Website material in any other media, selling, sublicensing and/or otherwise commercializing any Website material."},
                {"heading": "4. User Accounts", "content": "If you are provided with a user ID and password for this Website, you agree to keep your password confidential. You are responsible for all activities that occur under your user ID."},
                {"heading": "5. Content Liability", "content": "We shall not be hold responsible for any content that appears on your Website. You agree to protect and defend us against all claims that is rising on your Website."},
                {"heading": "6. Your Privacy", "content": "Please read our Privacy Policy to understand how we handle your personal information."},
                {"heading": "7. Reservation of Rights", "content": "We reserve the right to request that you remove all links or any particular link to our Website. You approve to immediately remove all links to our Website upon request."},
                {"heading": "8. Removal of links", "content": "If you find any link on our Website that is offensive for any reason, you are free to contact and inform us any moment. We will consider requests to remove links but we are not obligated to or so or to respond to you directly."},
                {"heading": "9. Disclaimer", "content": "To the maximum extent permitted by applicable law, we exclude all representations, warranties and conditions relating to our website and the use of this website."},
                {"heading": "10. Limitation of Liability", "content": "In no event shall XpertAI Global, nor any of its officers, directors and employees, be held liable for anything arising out of or in any way connected with your use of this Website."},
                {"heading": "11. Indemnification", "content": "You hereby indemnify to the fullest extent XpertAI Global from and against any and/or all liabilities, costs, demands, causes of action, damages and expenses arising in any way related to your breach of any of the provisions of these Terms."},
                {"heading": "12. Severability", "content": "If any provision of these Terms is found to be invalid under any applicable law, such provisions shall be deleted without affecting the remaining provisions herein."},
                {"heading": "13. Variation of Terms", "content": "XpertAI Global is permitted to revise these Terms at any time as it sees fit, and by using this Website you are expected to review these Terms on a regular basis."},
                {"heading": "14. Assignment", "content": "The XpertAI Global is allowed to assign, transfer, and subcontract its rights and/or obligations under these Terms without any notification. However, you are not allowed to assign, transfer, or subcontract any of your rights and/or obligations under these Terms."},
                {"heading": "15. Governing Law & Jurisdiction", "content": "These Terms will be governed by and interpreted in accordance with the laws of the State/Country of operation, and you submit to the non-exclusive jurisdiction of the state and federal courts located for the resolution of any disputes."},
                {"heading": "16. Entire Agreement", "content": "These Terms constitute the entire agreement between XpertAI Global and you in relation to your use of this Website, and supersede all prior agreements and understandings."}
            ]
        )

        # ==========================================
        # 3. REFUND POLICY (15 Sections)
        # ==========================================
        self.create_page(
            title="Refund & Cancellation Policy",
            slug="refund-policy",
            description="We want you to be satisfied with our services. Please read our refund and cancellation policy carefully.",
            sections=[
                {"heading": "1. General Refund Policy", "content": "We strive to ensure that our customers are satisfied with our services. However, due to the nature of digital and professional services, we have specific guidelines for refunds."},
                {"heading": "2. Service Cancellation", "content": "You may cancel a scheduled service consultation up to 24 hours before the appointment time for a full refund. Cancellations made within 24 hours may be subject to a cancellation fee."},
                {"heading": "3. Refund Eligibility", "content": "To be eligible for a refund, you must submit a request within 7 days of the purchase date. The service must not have been fully rendered or completed."},
                {"heading": "4. Non-refundable Services", "content": "Certain services, such as completed audits, filed tax returns, and personalized consultations that have already taken place, are non-refundable."},
                {"heading": "5. Processing Time", "content": "Once your refund request is received and inspected, we will send you an email to notify you of the approval or rejection of your refund. If approved, your refund will be processed within 7-10 business days."},
                {"heading": "6. Late or Missing Refunds", "content": "If you haven’t received a refund yet, first check your bank account again. Then contact your credit card company, it may take some time before your refund is officially posted."},
                {"heading": "7. Digital Products", "content": "We do not issue refunds for digital products (e.g., e-books, templates) once the order is confirmed and the product is sent. We recommend contacting us for assistance if you experience any issues receiving or downloading our products."},
                {"heading": "8. Subscription Cancellations", "content": "If you have a recurring subscription, you may cancel it at any time. You will continue to have access to the service through the end of your current billing period, but you will not be refunded for that period."},
                {"heading": "9. Exchanges", "content": "We only replace items if they are defective or damaged. If you need to exchange it for the same item, send us an email at support@xpertai.global."},
                {"heading": "10. Gifts", "content": "If the item was marked as a gift when purchased and shipped directly to you, you’ll receive a gift credit for the value of your return. Once the returned item is received, a gift certificate will be mailed to you."},
                {"heading": "11. Promotional Offers", "content": "Services purchased during a promotional sale or with a discount code may be refunded at the discounted price, not the full original price."},
                {"heading": "12. Force Majeure", "content": "We are not liable for refunds in cases where service delivery is prevented by circumstances beyond our control, including but not limited to natural disasters, government restrictions, or internet outages."},
                {"heading": "13. Chargebacks", "content": "You agree to contact us prior to raising a chargeback with your bank. Unjustified chargebacks may result in the suspension of your account and future services."},
                {"heading": "14. Dispute Resolution", "content": "If you believe a service was not delivered as promised, please raise a ticket via our Contact page within 3 days of service completion so we can investigate and resolve the issue."},
                {"heading": "15. Changes to Refund Policy", "content": "We reserve the right to modify this refund policy at any time. Changes and clarifications will take effect immediately upon their posting on the website."}
            ]
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded comprehensive Legal Pages."))

    def create_page(self, title, slug, description, sections):
        page, created = LegalPage.objects.get_or_create(
            slug=slug,
            defaults={'title': title, 'description': description}
        )
        
        if created:
            self.stdout.write(f"Created Page: {title}")
        else:
            self.stdout.write(f"Page exists: {title} (Updating sections...)")
            # Update title/desc if changed
            page.title = title
            page.description = description
            page.save()

        # Clear existing sections to avoid duplicates/stale data during re-runs
        page.sections.all().delete()

        for idx, section_data in enumerate(sections):
            LegalPageSection.objects.create(
                legal_page=page,  # Correct field name used here
                heading=section_data['heading'],
                content=section_data['content'],
                order=idx
            )