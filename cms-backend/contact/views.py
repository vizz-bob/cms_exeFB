from rest_framework import viewsets, mixins, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ContactMessage, ContactPage, OfficeAddress, Ticket
from .serializers import ContactSerializer, ContactPageSerializer, OfficeAddressSerializer, TicketSerializer

# --- 1. Public Data View ---
class ContactPageDataView(APIView):
    def get(self, request):
        content, _ = ContactPage.objects.get_or_create(id=1)
        addresses = OfficeAddress.objects.all().order_by('order')
        return Response({
            "content": ContactPageSerializer(content).data,
            "addresses": OfficeAddressSerializer(addresses, many=True).data,
        })

# --- 2. Public Form Submission ---
class ContactViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Public Endpoint: POST /api/contact/
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactSerializer

# --- 3. Admin CRUD ViewSets ---

class ContactPageViewSet(viewsets.ModelViewSet):
    queryset = ContactPage.objects.all()
    serializer_class = ContactPageSerializer

class OfficeAddressViewSet(viewsets.ModelViewSet):
    queryset = OfficeAddress.objects.all()
    serializer_class = OfficeAddressSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    Admin Endpoint: GET/DELETE /api/contact/messages/
    """
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer

class TicketViewSet(viewsets.ModelViewSet):
    """
    Admin Endpoint: GET/PUT/DELETE /api/contact/tickets/
    """
    serializer_class = TicketSerializer
    # IMPORTANT: Default queryset required for Router introspection
    queryset = Ticket.objects.all() 

    def get_queryset(self):
        """
        Custom logic to show tickets.
        """
        user = self.request.user
        
        # 1. Admin/Staff -> See ALL tickets
        if user.is_staff or user.is_superuser:
            return Ticket.objects.all().order_by('-created_at')
            
        # 2. Authenticated User -> See OWN tickets (matching email)
        if user.is_authenticated:
            return Ticket.objects.filter(email=user.email).order_by('-created_at')
            
        # 3. Fallback (e.g. for development if auth headers missing) -> Show All
        return Ticket.objects.all().order_by('-created_at')