from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from myShop.models import InfosProduit
from myShop.models import TransactionProduit
from myShop.serializers import InfosProduitSerializer
from myShop.serializers import TransactionProduitSerializer

from mytig.models import ProduitEnPromotion

from django.db.models.functions import ExtractYear

# Create your views here.
class RedirectionInfosProduit(APIView):
    """ /infoproduct/int:id/ """

    def get_object(self, id):
        try:
            return InfosProduit.objects.get(id = id)
        except InfosProduit.DoesNotExist:
            raise Http404

    def get(self, request, id, format = None):
        produit = self.get_object(id)
        serializer = InfosProduitSerializer(produit)
        return Response(serializer.data)

class RedirectionInfosProduitListe(APIView):
    """ /infoproducts/ """

    def get_object(self):
        try:
            return InfosProduit.objects.all()
        except InfosProduit.DoesNotExist:
            raise Http404

    def get(self, request, format = None):
        produits = self.get_object()
        serializer = InfosProduitSerializer(produits, many = True)
        return Response(serializer.data)

class RedirectionMiseEnPromoManuelle(APIView):
    """ /putonsale/int:id/str:newprice/ """

    def get_object(self, id):
        """ Tente la récupération d'un produit en promotion,
        renvoie None si le produit n'existe pas. """
        try:
            return InfosProduit.objects.get(id = id)
        except InfosProduit.DoesNotExist:
            raise Http404

    def get(self, request, id, newprice, format = None):
        """ Met le produit en promotion et renvoie le produit et sa remise. """
        try:
            InfosProduit.objects.filter(id = id).update(
                sale = True, discount = float(newprice))
        except Exception:
            return Response({'message': 'newprice doit être un flottant.'})

        produit = self.get_object(id)
        serializer = InfosProduitSerializer(produit)

        promoProduit = ProduitEnPromotion(id = id)
        promoProduit.save()

        return Response(serializer.data)

class RedirectionSuppressionPromoManuelle(APIView):
    """ /removesale/int:id/ """

    def get_object(self, id):
        try:
            return InfosProduit.objects.get(id = id)
        except InfosProduit.DoesNotExist:
            raise Http404

    def get(self, request, id, format = None):
        # Si un produit existe dans ProduitEnPromotion, on le supprime
        ProduitEnPromotion.objects.filter(id = id).delete()
        InfosProduit.objects.filter(id = id).update(
            sale = False, discount = 0.0)

        produit = self.get_object(id)
        serializer = InfosProduitSerializer(produit)
        return Response(serializer.data)

class RedirectionAugmentationStock(APIView):
    """ /incrementstock/int:id/int:number/ """

    def get_object(self, id):
        try:
            return InfosProduit.objects.get(id = id)
        except InfosProduit.DoesNotExist:
            raise Http404

    def get(self, request, id, number, format = None):
        produit = self.get_object(id)
        InfosProduit.objects.filter(id = id).update(
            quantityInStock = produit.quantityInStock + number)
        produit.refresh_from_db()
        serializer = InfosProduitSerializer(produit)
        return Response(serializer.data)

class RedirectionDiminutionStock(APIView):
    """ /decrementstock/int:id/int:number/ """

    def get_object(self, id):
        try:
            return InfosProduit.objects.get(id = id)
        except Exception:
            raise Http404

    def get(self, request, id, number, format = None):
        produit = self.get_object(id)

        # Parti pris de dire qu'un nombre supérieur à quantityInStock revient à
        # supprimer l'entièreté du stock
        if number > produit.quantityInStock:
            InfosProduit.objects.filter(id = id).update(quantityInStock = 0)
        else:
            InfosProduit.objects.filter(id = id).update(
                quantityInStock = produit.quantityInStock - number)
            produit.refresh_from_db()

        serializer = InfosProduitSerializer(produit)
        return Response(serializer.data)

class RedirectionAjoutTransaction(APIView):
    """ /transaction/int:tigID/str:type/str:price/str:quantity/ """

    def get(self, request, tigID, type, price, quantity, format = None):
        try:
            transac = TransactionProduit(
                tigID = tigID, type = type, price = float(price), quantity = int(quantity))
            transac.save()
        except Exception:
            return Response({"message": "price doit être un flottant"})

        serializer = TransactionProduitSerializer(transac)
        return Response(serializer.data)

class RedirectionTransactionAnnee(APIView):
    """ /transaction/getannee/int:annee/ """

    def get_object(self, annee):
        try:
            return TransactionProduit.objects.filter(
                date__year = annee, type = "vente")
        except TransactionProduit.DoesNotExist:
            raise Http404

    def get(self, request, annee, format = None):
        transac = self.get_object(annee)
        serializer = TransactionProduitSerializer(transac, many = True)
        return Response(serializer.data)

class RedirectionTransactionTrimestre(APIView):
    """ /transaction/gettrimestre/int:annee/int:trimestre/ """

    def get_object(self, annee, trimestre):
        try:
            return TransactionProduit.objects.filter(
                date__year = annee, date__quarter = trimestre, type = "vente")
        except TransactionProduit.DoesNotExist:
            raise Http404

    def get(self, request, annee, trimestre, format = None):
        transac = self.get_object(annee, trimestre)
        serializer = TransactionProduitSerializer(transac, many = True)
        return Response(serializer.data)

class RedirectionTransactionMois(APIView):
    """ /transaction/getmois/int:annee/int:mois/ """

    def get_object(self, annee, mois):
        try:
            return TransactionProduit.objects.filter(
                date__year = annee, date__month = mois, type = "vente")
        except TransactionProduit.DoesNotExist:
            raise Http404

    def get(self, request, annee, mois, format = None):
        transac = self.get_object(annee, mois)
        serializer = TransactionProduitSerializer(transac, many = True)
        return Response(serializer.data)

class RedirectionTransactionJour(APIView):
    """ /transaction/getjour/int:annee/int:mois/int:jour/ """

    def get_object(self, annee, mois, jour):
        try:
            return TransactionProduit.objects.filter(
                date__year = annee, date__month = mois, date__day = jour, type = "vente")
        except TransactionProduit.DoesNotExist:
            raise Http404

    def get(self, request, annee, mois, jour, format = None):
        transac = self.get_object(annee, mois, jour)
        serializer = TransactionProduitSerializer(transac, many = True)
        return Response(serializer.data)
